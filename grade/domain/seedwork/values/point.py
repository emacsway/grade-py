import typing
from abc import ABCMeta, abstractmethod
from decimal import Decimal

from geopy import Point as _Point

from ..utils import setterproperty

__all__ = ('Point', 'IPointExporterSetter',)


# TODO: Fix interface
class Point(_Point):

    def __new__(cls, latitude: Decimal, longitude: Decimal, altitude: typing.Optional[Decimal] = None):
        if latitude is None and longitude is None and altitude is None:
            return EmptyPoint()
        return super().__new__(cls, latitude, longitude, altitude)

    def export(self, exporter: 'IPointExporterSetter'):
        exporter.longitude = Decimal(self.longitude).quantize(Decimal(".000001"))
        exporter.latitude = Decimal(self.latitude).quantize(Decimal(".000001"))
        exporter.altitude = bool(self.altitude) and Decimal(self.altitude).quantize(Decimal(".000001")) or None

    @staticmethod
    def empty():
        return EmptyPoint()

    @property
    def is_empty(self):
        return self == EmptyPoint()


class EmptyPoint(Point):

    def __new__(cls):
        return _Point.__new__(cls)

    def export(self, exporter: 'IPointExporterSetter'):
        exporter.longitude = None
        exporter.latitude = None
        exporter.altitude = None


class IPointExporterSetter(metaclass=ABCMeta):

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
    def altitude(self, value: Decimal):
        raise NotImplementedError
