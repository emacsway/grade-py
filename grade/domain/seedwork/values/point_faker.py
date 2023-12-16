import typing
from decimal import Decimal
from .point import Point
from ..faker import Faker


__all__ = ('PointFaker', )


class PointFaker:
    longitude: typing.Optional[Decimal]
    latitude: typing.Optional[Decimal]

    def __init__(self, **kwargs):
        self._faker = Faker()
        self._fake(**kwargs)

    def _fake(self, **kwargs):
        self.latitude = kwargs.get('latitude') or self._faker.latitude()
        self.longitude = kwargs.get('upper') or self._faker.longitude()

    def next(self):
        self._fake()

    def create(self) -> Point:
        return Point(self.latitude, self.longitude)
