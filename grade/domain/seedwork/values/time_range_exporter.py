import datetime

from ..utils import setterproperty
from .time_range import ITimeRangeExporterSetter

__all__ = ('TimeRangeExporter', )


class TimeRangeExporter(ITimeRangeExporterSetter):
    def __init__(self):
        self.data = dict()

    @setterproperty
    def lower(self, value: datetime.datetime):
        self.data['lower'] = value

    @setterproperty
    def upper(self, value: datetime.datetime):
        self.data['upper'] = value
