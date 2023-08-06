from __future__ import annotations

import copy
from typing import Any, Callable, Dict, Iterable, Iterator, List, Optional, Union

from glitter_proto.blockved.glitterchain.index import Argument as Argument_pb

from glitter_sdk.util.json import JSONSerializable

from .argument import Argument


class Arguments(JSONSerializable, List[Argument_pb]):
    """Represents an unordered collection of :class:`Argument` objects
    -- analagous to ``sdk.Arguments`` and ``sdk.DecCoins`` in Cosmos SDK. If one of the
    input Arguments would be ``Dec``-amount type Argument, the resultant Arguments is converted to
    ``Dec``-amount Arguments.

    Args:
        arg (Optional[Arguments.Input], optional): argument to convert. Defaults to ``{}``.

    Raises:
        TypeError: if ``arg`` is not an Iterable
    """

    Input = Union[Iterable[Argument],  Dict[str, Argument]]
    """Types which can be converted into a :class:`Arguments` object."""

    _arguments: Dict[str, Argument]

    def __repr__(self) -> str:
        if len(self) == 0:
            return "Arguments()"
        else:
            return f"Arguments('{self!s}')"

    def __str__(self) -> str:
        return ",".join(str(Argument) for Argument in self)

    def __init__(self, arg: Optional[Arguments.Input] = {}, **denoms):
        """Converts the argument into a :class:`Arguments` object."""

        if arg is None:
            self._arguments = {}
            return

        # arg should be an iterable
        try:
            iter(arg)
        except TypeError:
            raise TypeError(f"could not create Arguments object with argument: {arg!s}")

        if isinstance(arg, Arguments):
            self._arguments = copy.deepcopy(arg._arguments)
            return

        self._arguments = Arguments(denoms)._arguments if denoms else {}

        arguments: Iterable[Argument]
        if isinstance(arg, dict):
            arguments = [Argument(denom, arg[denom]) for denom in arg]
        else:
            arguments = arg
        for argument in arguments:
            self._arguments[argument.denom] = argument

        # make all Arguments DecCoin if one is DecCoin
        if not all([c.is_int_coin() for c in self]):
            for denom in self._arguments:
                self._arguments[denom] = self._arguments[denom].to_dec_coin()

    def __getitem__(self, denom: str) -> Argument:
        return self._arguments[denom]

    def get(self, denom: str) -> Optional[Argument]:
        """Get the Argument with the denom contained in the Arguments set.

        Args:
            denom (str): denom

        Returns:
            Optional[Argument]: result (can be ``None``)
        """
        return self._arguments.get(denom)

    @classmethod
    def from_proto(cls, proto: List[Argument_pb]) -> Arguments:
        """Converts list of Argument-data objects to :class:`Arguments`.

        Args:
            data (list): list of Argument-data objects
        """
        Arguments = map(Argument.from_proto, proto)
        return cls(Arguments)

    def to_proto(self) -> List[Argument_pb]:
        return [Argument.to_proto() for Argument in self]

    def to_list(self) -> List[Argument]:
        """Converts the set of :class:`Coin` objects contained into a sorted list by denom.

        Returns:
            List[Coin]: list, sorted by denom
        """
        return sorted(self._arguments.values(), key=lambda c: c.denom)

    def __eq__(self, other) -> bool:
        try:
            return self.to_list() == other.to_list()
        except AttributeError:
            return False

    def __iter__(self):
        return iter(self.to_list())

    def __len__(self):
        return len(self.to_list())

    def __contains__(self, denom: str) -> bool:
        return denom in self._arguments
