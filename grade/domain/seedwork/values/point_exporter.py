from decimal import Decimal
from ..utils import setterproperty
from .point import IPointExporterSetter

__all__ = ('PointExporter', )


class PointExporter(IPointExporterSetter):
    def __init__(self):
        self.data = dict()

    @setterproperty
    def longitude(self, value: Decimal):
        self.data['longitude'] = value

    @setterproperty
    def latitude(self, value: Decimal):
        self.data['latitude'] = value
