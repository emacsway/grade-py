import typing
import datetime
from ..faker import Faker
from .time_range import TimeRange


__all__ = ('TimeRangeFaker', )


class TimeRangeFaker:
    lower: typing.Optional[datetime.datetime]
    upper: typing.Optional[datetime.datetime]
    delta: datetime.timedelta = datetime.timedelta(hours=8)

    def __init__(self, **kwargs):
        self._faker = Faker()
        self._fake(**kwargs)

    def _fake(self, **kwargs):
        self.lower = kwargs.get('lower') or self._faker.date_time()
        self.upper = kwargs.get('upper') or self._faker.date_time_between_dates(
            datetime_start=self.lower,
            datetime_end=getattr(self, 'upper', self.delta)
        )

    def next(self):
        self._fake()

    def create(self):
        return TimeRange(self.lower, self.upper)
