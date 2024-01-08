import typing
from decimal import Decimal
from .geolocation_coordinates import GeolocationCoordinates
from ..faker import Faker


__all__ = ('GeolocationCoordinatesFaker', )


class GeolocationCoordinatesFaker:
    longitude: typing.Optional[Decimal]
    latitude: typing.Optional[Decimal]
    altitude: typing.Optional[Decimal] = None
    accuracy: typing.Optional[Decimal] = None
    altitude_accuracy: typing.Optional[Decimal] = None
    heading: typing.Optional[Decimal] = None
    speed: typing.Optional[Decimal] = None

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

    async def create(self) -> GeolocationCoordinates:
        return GeolocationCoordinates(self.latitude, self.longitude)

    def to_dict(self):
        return dict(
            latitude=self.latitude,
            longitude=self.longitude,
            altitude=self.altitude,
            accuracy=self.accuracy,
            altitude_accuracy=self.altitude_accuracy,
            heading=self.heading,
            speed=self.speed,
        )
