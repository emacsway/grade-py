"""
See https://developer.mozilla.org/en-US/docs/Web/API/GeolocationCoordinates
"""
import typing
from abc import ABCMeta, abstractmethod
from decimal import Decimal
from geopy.distance import geodesic

from ..utils import setterproperty
from .point import Point

__all__ = ('GeolocationCoordinates', 'IGeolocationCoordinatesExporterSetter', )


class GeolocationCoordinates:
    _latitude: Decimal
    _longitude: Decimal
    _altitude: typing.Optional[Decimal] = None
    _accuracy: typing.Optional[Decimal] = None
    _altitude_accuracy: typing.Optional[Decimal] = None
    _heading: typing.Optional[Decimal] = None
    _speed: typing.Optional[Decimal] = None

    def __init__(
        self,
        latitude: Decimal,
        longitude: Decimal,
        altitude: typing.Optional[Decimal] = None,
        accuracy: typing.Optional[Decimal] = None,
        altitude_accuracy: typing.Optional[Decimal] = None,
        heading: typing.Optional[Decimal] = None,
        speed: typing.Optional[Decimal] = None,
    ):
        self._latitude = latitude
        self._longitude = longitude
        self._altitude = altitude
        self._accuracy = accuracy
        self._altitude_accuracy = altitude_accuracy
        self._heading = heading
        self._speed = speed

    @property
    def point(self) -> Point:
        return Point(self._latitude, self._longitude, self._altitude)

    def distance(self, location: Point):
        return geodesic(self.point, location).m - (float(self._accuracy) if self._accuracy else 0)

    def export(self, exporter: 'IGeolocationCoordinatesExporterSetter'):
        exporter.latitude = self._latitude
        exporter.longitude = self._longitude
        exporter.altitude = self._altitude
        exporter.accuracy = self._accuracy
        exporter.altitude_accuracy = self._altitude_accuracy
        exporter.heading = self._heading
        exporter.speed = self._speed


class IGeolocationCoordinatesExporterSetter(metaclass=ABCMeta):

    @setterproperty
    @abstractmethod
    def longitude(self, value: Decimal):
        raise NotImplementedError

    @setterproperty
    @abstractmethod
    def latitude(self, value: Decimal):
        raise NotImplementedError

    @setterproperty
    @abstractmethod
    def altitude(self, value: typing.Optional[Decimal]):
        raise NotImplementedError

    @setterproperty
    @abstractmethod
    def accuracy(self, value: typing.Optional[Decimal]):
        raise NotImplementedError

    @setterproperty
    @abstractmethod
    def altitude_accuracy(self, value: typing.Optional[Decimal]):
        raise NotImplementedError

    @setterproperty
    @abstractmethod
    def heading(self, value: typing.Optional[Decimal]):
        raise NotImplementedError

    @setterproperty
    @abstractmethod
    def speed(self, value: typing.Optional[Decimal]):
        raise NotImplementedError
