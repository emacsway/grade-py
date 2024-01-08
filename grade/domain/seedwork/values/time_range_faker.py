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
        self.lower = kwargs['lower'] if 'lower' in kwargs else self._faker.date_time()
        self.upper = kwargs['upper'] if 'upper' in kwargs else self._faker.date_time_between_dates(
            datetime_start=self.lower,
            datetime_end=self.lower + self.delta
        )

    async def next(self):
        self._fake()

    async def create(self):
        return TimeRange(self.lower, self.upper)

    def to_dict(self):
        return dict(
            lower=self.lower,
            upper=self.upper,
        )
