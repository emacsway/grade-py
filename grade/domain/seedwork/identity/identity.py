import typing

from ..specification import IEqualOperand
from ..aggregate import IHashable
from .interfaces import IAccessible

__all__ = ('Identity', )


T = typing.TypeVar('T')


class Identity(typing.Generic[T], IAccessible[T], IHashable):

    def __init__(self, value: typing.Optional[T]):
        self._value = value

    @property
    def value(self) -> T:
        return self._value

    def is_transient(self) -> bool:
        return self._value is None

    @classmethod
    def transient(cls):
        return cls(None)

    def __hash__(self) -> int:
        return hash(self._value)

    def __eq__(self, other: IEqualOperand):
        assert isinstance(other, Identity)
        return self._value == other._value

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self._value)

    def export(self, setter: typing.Callable[[T], None]):
        setter(self._value)
