from __future__ import annotations

import math
import re
from typing import Union

import attr
from glitter_proto.blockved.glitterchain.index import Argument as Argument_pb
from glitter_proto.blockved.glitterchain.index import ArgumentVarType as ArgumentVarType_pb

from glitter_sdk.util.json import JSONSerializable



@attr.s(frozen=True)
class Argument(JSONSerializable):
    """Represents a (type, value) pairing, analagous to ``sdk.Argument`` and ``sdk.DecCoin``
    in Cosmos SDK. Used for representing Glitter native assets.
    """
    type: ArgumentVarType_pb = attr.ib()
    """Argument's denomination, only ``uluna``."""

    value: bytes = attr.ib()  # type: ignore
    """Argument's value -- can be a ``int`` or :class:`Dec`"""

    @classmethod
    def from_proto(cls, proto: Argument_pb) -> Argument:
        return cls(proto.type, proto.value)

    def to_proto(self) -> Argument_pb:
        Argument = Argument_pb()
        Argument.type = self.type
        Argument.value = str(self.value)
        return Argument
