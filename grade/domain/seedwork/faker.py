import uuid
import typing
import datetime
from decimal import Decimal
from dateutil import tz

from faker import Faker as _Faker


DateParseType = typing.Union[datetime.date, datetime.datetime, datetime.timedelta, str, int]


class Faker:

    def __init__(self):
        self.__faker = _Faker()
        self._sequence = 0

    def company(self) -> str:
        return self.__faker.company()

    def sequence(self) -> int:
        self._sequence += 1
        return self._sequence

    def uuid(self) -> uuid.UUID:
        return uuid.uuid4()

    def date_time(self, before_now: bool = True, after_now: bool = False) -> datetime.datetime:
        return self.__faker.date_time_this_month(
            before_now=before_now,
            after_now=after_now,
            tzinfo=tz.tzutc()
        ).replace(microsecond=0)

    def date_time_between_dates(self, datetime_start: typing.Optional[DateParseType] = None,
                                datetime_end: typing.Optional[DateParseType] = None) -> datetime.datetime:
        return self.__faker.date_time_between_dates(
            datetime_start=datetime_start,
            datetime_end=datetime_end,
            tzinfo=tz.tzutc()
        ).replace(microsecond=0)

    def latitude(self) -> Decimal:
        return self.__faker.latitude().quantize(Decimal(".000001"))

    def longitude(self) -> Decimal:
        return self.__faker.longitude().quantize(Decimal(".000001"))

    def local_latlng(self, country_code: str = 'RU') -> tuple[Decimal, Decimal]:
        result = self.__faker.local_latlng(country_code, coords_only=True)
        result = tuple(map(
            lambda coord: Decimal(coord).quantize(Decimal(".000001")),
            result
        ))
        result = typing.cast(tuple[Decimal, Decimal], result)
        return result
