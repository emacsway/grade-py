import datetime

from abc import ABCMeta, abstractmethod
from psycopg.types.range import TimestamptzRange

from ..utils import setterproperty


__all__ = ('TimeRange', 'ITimeRangeExporterSetter',)


# TODO: Fix interface
class TimeRange(TimestamptzRange):

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
