import typing
from decimal import Decimal
from ..utils import setterproperty
from .geolocation_coordinates import IGeolocationCoordinatesExporterSetter

__all__ = ('GeolocationCoordinatesExporter', )


class GeolocationCoordinatesExporter(IGeolocationCoordinatesExporterSetter):
    def __init__(self):
        self.data = dict()

    @setterproperty
    def longitude(self, value: Decimal):
        self.data['longitude'] = value

    @setterproperty
    def latitude(self, value: Decimal):
        self.data['latitude'] = value

    @setterproperty
    def altitude(self, value: typing.Optional[Decimal]):
        self.data['latitude'] = value

    @setterproperty
    def accuracy(self, value: typing.Optional[Decimal]):
        self.data['latitude'] = value

    @setterproperty
    def altitude_accuracy(self, value: typing.Optional[Decimal]):
        self.data['latitude'] = value

    @setterproperty
    def heading(self, value: typing.Optional[Decimal]):
        self.data['latitude'] = value

    @setterproperty
    def speed(self, value: typing.Optional[Decimal]):
        self.data['latitude'] = value
