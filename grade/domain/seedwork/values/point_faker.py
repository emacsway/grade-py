import typing
from decimal import Decimal
from .point import Point
from ..faker import Faker


__all__ = ('PointFaker', )


class PointFaker:
    longitude: Decimal
    latitude: Decimal
    altitude: typing.Optional[Decimal] = None

    def __init__(self, **kwargs):
        self._faker = Faker()
        self._fake(**kwargs)

    def _fake(self, **kwargs):
        if kwargs:
            self.latitude = kwargs.get('latitude') or self._faker.latitude()
            self.longitude = kwargs.get('longitude') or self._faker.longitude()
        else:
            self.latitude, self.longitude = self._faker.local_latlng()

    async def next(self):
        self._fake()

    async def create(self) -> Point:
        return Point(self.latitude, self.longitude)

    @classmethod
    def empty(cls):
        return EmptyPointFaker()

    def to_dict(self):
        return dict(
            latitude=self.latitude,
            longitude=self.longitude,
            altitude=self.altitude,
        )


class EmptyPointFaker(PointFaker):
    longitude = None
    latitude = None
    altitude = None

    def __init__(self, **kwargs):
        pass

    async def next(self):
        pass

    async def create(self) -> Point:
        return Point.empty()
