from __future__ import annotations

import requests
import base64
import glitter_proto.blockved.glitterchain.index
from glitter_sdk.key.key import Key, SignOptions
from glitter_sdk.core.tx import SignMode, Tx
from glitter_sdk.core.msgs import SQLExecRequest, SQLGrantRequest
from glitter_sdk.util.url import urljoin
from glitter_sdk.util.parse_sql import escape_args
from glitter_sdk.exceptions import *
from glitter_sdk.client.lcd.api.tx import CreateTxOptions, SignerOptions
from glitter_proto.blockved.glitterchain.index import *
from glitter_sdk.core.bank import MsgMultiSend, MsgSend

__all__ = ["DB", "AsyncDB"]

GrantReader = "reader"
GrantWriter = "writer"
GrantAdmin = "admin"
WriteLimitRow = 50


class AsyncDB:
    def __init__(self, lcd, key: Key):
        self.lcd = lcd
        self.key = key

    async def account_number(self) -> int:
        res = await self.lcd.auth.account_info(self.key.acc_address)
        return res.account_number

    async def sequence(self) -> int:
        res = await self.lcd.auth.account_info(self.key.acc_address)
        return res.sequence

    async def account_number_and_sequence(self) -> dict:
        res = await self.lcd.auth.account_info(self.key.acc_address)
        return {"account_number": res.get_account_number(), "sequence": res.get_sequence()}

    async def create_tx(self, options: CreateTxOptions) -> Tx:
        sigOpt = [
            SignerOptions(
                address=self.key.acc_address,
                sequence=options.sequence,
                public_key=self.key.public_key,
            )
        ]
        return await self.lcd.tx.create(sigOpt, options)

    async def create_and_sign_tx(self, options: CreateTxOptions) -> Tx:
        account_number = options.account_number
        sequence = options.sequence
        if account_number is None or sequence is None:
            res = await self.account_number_and_sequence()
            if account_number is None:
                account_number = res.get("account_number")
            if sequence is None:
                sequence = res.get("sequence")
        options.sequence = sequence
        options.account_number = account_number
        return self.key.sign_tx(
            tx=(await self.create_tx(options)),
            options=SignOptions(
                account_number=account_number,
                sequence=sequence,
                chain_id=self.lcd.chain_id,
                sign_mode=options.sign_mode
                if options.sign_mode
                else SignMode.SIGN_MODE_DIRECT,
            ),
        )


class DB:
    """Wraps around a :class:`Key` implementation and provides transaction building and
    signing functionality. It is recommended to create this object through
    :meth:`LCDClient.DB()<glitter_sdk.client.lcd.LCDClient.DB>`."""

    def __init__(self, lcd, key: Key):
        self.lcd = lcd
        self.key = key

    def account_number(self) -> int:
        """Fetches account number for the account associated with the Key."""
        res = self.lcd.auth.account_info(self.key.acc_address)
        return res.account_number

    def sequence(self) -> int:
        """Fetches the sequence number for the account associated with the Key."""
        res = self.lcd.auth.account_info(self.key.acc_address)
        return res.sequence

    def account_number_and_sequence(self) -> dict:
        """Fetches both account and sequence number associated with the Key."""
        k = self.key.acc_address
        res = self.lcd.auth.account_info(self.key.acc_address)
        return {"account_number": res.get_account_number(), "sequence": res.get_sequence()}

    def create_tx(self, options: CreateTxOptions) -> Tx:
        """Builds an unsigned transaction object. The ``DB`` will first
        query the blockchain to fetch the latest ``account`` and ``sequence`` values for the
        account corresponding to its Key, unless the they are both provided. If no ``fee``
        parameter is set, automatic fee estimation will be used (see `fee_estimation`).

        Args:
            options (CreateTxOptions): Options to create a tx

        Returns:
            Tx: unsigned transaction
        """
        sigOpt = [
            SignerOptions(
                address=self.key.acc_address,
                sequence=options.sequence,
                public_key=self.key.public_key,
            )
        ]
        return self.lcd.tx.create(sigOpt, options)

    def create_and_sign_tx(self, options: CreateTxOptions) -> Tx:
        """Creates and signs a :class:`Tx` object in a single step. This is the recommended
        method for preparing transaction for immediate signing and broadcastring. The transaction
        is generated exactly as :meth:`create_tx`.

        Args:
            options (CreateTxOptions): Options to create a tx

        Returns:
            Tx: signed transaction
        """

        account_number = options.account_number
        sequence = options.sequence
        if account_number is None or sequence is None:
            res = self.account_number_and_sequence()
            if account_number is None:
                account_number = res.get("account_number")
            if sequence is None:
                sequence = res.get("sequence")
        options.sequence = sequence
        options.account_number = account_number
        return self.key.sign_tx(
            tx=self.create_tx(options),
            options=SignOptions(
                account_number=account_number,
                sequence=sequence,
                chain_id=self.lcd.chain_id,
                sign_mode=options.sign_mode
                if options.sign_mode
                else SignMode.SIGN_MODE_DIRECT,
            ),
        )

    def sql_exec(self, sql):
        tx = self.create_and_sign_tx(CreateTxOptions(
            msgs=[SQLExecRequest(
                self.key.acc_address,
                sql,
            )],
            # fee=Fee(300000, "15stake"),
            memo="sql transaction!",
            fee_denoms=["agli"],
            sign_mode=SignMode.SIGN_MODE_DIRECT,
            gas="auto",
        ))
        return self.lcd.tx.broadcast(tx)

    def create_database(self, database):
        sql = "CREATE DATABASE IF NOT EXISTS {} ".format(database)
        return self.sql_exec(sql)

    def create_table(self, sql):
        return self.sql_exec(sql)

    def drop_table(self, database: str, table: str):
        sql = "DROP TABLE IF EXISTS {}.{} ".format(database, table)
        return self.sql_exec(sql)

    # only suport standard engine
    def add_column(self, database: str, table: str, col: str):
        sql = "ALTER TABLE {}.{} ADD {} ".format(database, table, col)
        return self.sql_exec(sql)

    def show_create_table(self, database: str, table: str):
        endpoint = "/blockved/glitterchain/index/sql/show_create_table"
        req = ShowCreateTableRequest()
        req.database_name = database
        req.table_name = table
        r = requests.get(urljoin(self.lcd.url, endpoint), req.to_dict())
        if r.status_code != 200:
            raise LCDResponseError(message=r.text, response=r)
        response = ShowCreateTableResponse().from_dict(r.json())
        return response

    def list_databases(self, creator: str = None):
        endpoint = "/blockved/glitterchain/index/sql/list_databases"
        r = requests.get(urljoin(self.lcd.url, endpoint))
        if r.status_code != 200:
            raise LCDResponseError(message=str(r.status_code), response=r)

        result = SqlListDatabasesResponse()
        response = SqlListDatabasesResponse().from_dict(r.json())
        for  db in response.databases:
            if creator and creator != db.creator:
                continue
            result.databases.append(db)
        return result

    def list_tables(self, table_keyword: str = None, uid: str = None, database: str = None,
                    page: int = None, page_size: int = None):
        endpoint = "/blockved/glitterchain/index/sql/list_tables"

        payload = {}
        if table_keyword is not None:
            payload["keyword"] = table_keyword
        if uid is not None:
            payload["uid"] = uid
        if database is not None:
            payload["database"] = database
        if page is not None:
            payload["page"] = page
        if page_size is not None:
            payload["page_size"] = page_size

        r = requests.get(urljoin(self.lcd.url, endpoint), payload)
        if r.status_code != 200:
            raise LCDResponseError(message=str(r.status_code), response=r)
        return SqlListTablesResponse().from_dict(r.json())

    def insert(self, table: str, columns: map):
        col_name = list(columns.keys())
        place_hold = []
        vals = []
        for idx in col_name:
            place_hold.append('%s')
            vals.append(columns[idx])
        vals = escape_args(vals)

        sql = "insert into {} ({}) values ({})".format(table, ",".join(col_name), ",".join(place_hold))
        stmt = sql % vals
        return self.sql_exec(stmt)

    def batch_insert(self, db: str, table: str, rows: list = None):
        if not rows:
            raise ParamError("rows is empty")

        col_names = rows[0].keys()
        row_len = len(rows)
        col_len = len(col_names)
        place_hold = []
        vals = []
        for row_idx in range(0, row_len):
            place_hold_arr = ['%s'] * col_len
            place_hold.append("(" + ",".join(place_hold_arr) + ")")

        for row in rows:
            for col_name in col_names:
                vals.append(row[col_name])
        vals = escape_args(vals)

        sql = "INSERT INTO {}.{} ({}) VALUES {}".format(db, table, ",".join(col_names),
                                                        ",".join(place_hold))
        stmt = sql % vals
        return self.sql_exec(stmt)

    def update(self, database_name: str, table_name: str, columns: map = None, where: map = None):
        if not columns:
            raise ParamError("columns is empty")

        update = []
        for col_name, col_val in columns.items():
            update.append("{}={}".format(col_name, escape_args(col_val)))

        sql = "UPDATE  {}.{} SET {} ".format(database_name, table_name, ",".join(update))

        where_cond = []
        if where:
            for col_name, col_val in where.items():
                where_cond.append("{}{}".format(col_name, escape_args(col_val)))
            sql += " WHERE {}".format(" AND ".join(where_cond))

        return self.sql_exec(sql)

    def delete(self, database_name: str, table_name: str, where: map, order_by: str = None,
               asc: bool = True, limit: int = WriteLimitRow):
        if not where:
            raise ParamError("where is empty")
        if limit > WriteLimitRow:
            raise ParamError("too much will to delete")

        sql = "DELETE FROM {}.{} ".format(database_name, table_name)

        where_cond = []
        if where:
            for col_name, col_val in where.items():
                where_cond.append("{}{}".format(col_name, escape_args(col_val)))
            sql += " WHERE {}".format(" AND ".join(where_cond))

        if order_by:
            sql += " ORDER BY {} {}".format(order_by, "ASC" if asc else "DESC")

        sql += " LIMIT {}".format(limit)

        return self.sql_exec(sql)

    def query(self, sql: str):
        endpoint = "/blockved/glitterchain/index/sql/simple_query"
        req = SqlQueryRequest()
        req.sql = sql
        r = requests.post(urljoin(self.lcd.url, endpoint), data=req.to_json(), timeout=10)
        if r.status_code != 200:
            raise LCDResponseError(message=r.text, response=str(r.status_code))
        response = SimpleSqlQueryResponse().from_dict(r.json())
        row_set = []
        for raw_row in response.result:
            row = {}
            for field_name, col_val in raw_row.row.items():
                value_type = col_val.column_value_type
                if value_type == ColumnValueType.IntColumn or value_type == ColumnValueType.UintColumn:
                    row[field_name] = int(col_val.value)
                elif value_type == ColumnValueType.FloatColumn:
                    row[field_name] = float(col_val.value)
                elif value_type == ColumnValueType.BoolColumn:
                    row[field_name] = bool(col_val.value)
                elif value_type == ColumnValueType.StringColumn:
                    row[field_name] = col_val.value
                elif value_type == ColumnValueType.BytesColumn:
                    row[field_name] = base64.b64decode(col_val.value)
                elif value_type == ColumnValueType.InvalidColumn:
                    row[field_name] = col_val.value
            row_set.append(row)
        return row_set

    def sql_grant(self, to_addr: str, role: str, database: str, table: str = None):
        grantRequest = SQLGrantRequest(
            self.key.acc_address,
            to_addr,
            role,
            database
        )
        if table:
            grantRequest.on_table = table

        tx = self.create_and_sign_tx(CreateTxOptions(
            msgs=[grantRequest],
            # fee=Fee(300000, "15agli"),
            memo="grant transaction!",
            fee_denoms=["agli"],
            sign_mode=SignMode.SIGN_MODE_DIRECT
        ))
        return self.lcd.tx.broadcast(tx)

    def grant_reader(self, to_addr: str, database: str, table: str = None):
        return self.sql_grant(to_addr, GrantReader, database, table)

    def grant_writer(self, to_addr: str, database: str, table: str = None):
        return self.sql_grant(to_addr, GrantWriter, database, table)

    def grant_admin(self, to_addr: str, database: str, table: str = None):
        return self.sql_grant(to_addr, GrantAdmin, database, table)

    def transfer(self, addr: str, amount: str):
        tx = self.create_and_sign_tx(CreateTxOptions(
            msgs=[MsgSend(
                self.key.acc_address,
                addr,
                amount
            )],
            # fee=Fee(300000, "15stake"),
            memo="ban send transaction!",
            fee_denoms=["agli"],
            sign_mode=SignMode.SIGN_MODE_DIRECT,
            gas="auto",
        ))
        return self.lcd.tx.broadcast(tx)
