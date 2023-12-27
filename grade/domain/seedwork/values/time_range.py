import typing
import datetime

from abc import ABCMeta, abstractmethod
from psycopg.types.range import TimestamptzRange

from ..utils import setterproperty


__all__ = ('TimeRange', 'ITimeRangeExporterSetter',)


# TODO: Fix interface
class TimeRange(TimestamptzRange):

    def __init__(
        self,
        lower: typing.Optional[datetime.datetime] = None,
        upper: typing.Optional[datetime.datetime] = None,
    ):
        if lower and not isinstance(lower, datetime.datetime):
            raise ValueError("Type of IntIdentity value should be str, not %r", (lower, ))

        if upper and not isinstance(upper, datetime.datetime):
            raise ValueError("Type of IntIdentity value should be str, not %r", (upper, ))

        if lower and upper:
            if lower > upper:
                raise ValueError(
                    "Range lower %s bound must be less than or equal to range upper %s bound", (lower, upper)
                )
        super().__init__(lower, upper)

    def export(self, exporter: 'ITimeRangeExporterSetter'):
        exporter.lower = self.lower
        exporter.upper = self.upper


class ITimeRangeExporterSetter(metaclass=ABCMeta):

    @setterproperty
    @abstractmethod
    def lower(self, value: datetime.datetime):
        raise NotImplementedError

    @setterproperty
    @abstractmethod
    def upper(self, value: datetime.datetime):
        raise NotImplementedError
