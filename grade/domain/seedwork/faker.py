import typing
import datetime
from decimal import Decimal

from faker import Faker as _Faker


DateParseType = typing.Union[datetime.date, datetime.datetime, datetime.timedelta, str, int]


class Faker:

    def __init__(self):
        self.__faker = _Faker()

    def date_time(self, before_now: bool = True, after_now: bool = False) -> datetime.datetime:
        return self.__faker.date_time_this_month(before_now=before_now, after_now=after_now)

    def date_time_between_dates(self, datetime_start: typing.Optional[DateParseType] = None,
                                datetime_end: typing.Optional[DateParseType] = None) -> datetime.datetime:
        return self.__faker.date_time_between_dates(datetime_start=datetime_start, datetime_end=datetime_end)

    def latitude(self) -> Decimal:
        return self.__faker.latitude().quantize(Decimal(".000001"))

    def longitude(self) -> Decimal:
        return self.__faker.longitude().quantize(Decimal(".000001"))
