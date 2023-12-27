import typing
from abc import ABCMeta, abstractmethod
from .interfaces import IVersionedAggregate

from ..utils import setterproperty


__all__ = ('VersionedAggregate', 'IVersionedAggregateExporterSetter', 'IVersionedAggregateImporterGetter', )


class VersionedAggregate(IVersionedAggregate, metaclass=ABCMeta):

    def __init__(self, version: int = 0, **kwargs):
        self.__version = version
        super().__init__(**kwargs)

    @property
    def version(self) -> int:
        return self.__version

    @version.setter
    def version(self, value: int):
        self.__version = value

    def next_version(self) -> int:
        self.__version += 1
        return self.__version

    def export(self, exporter: 'IVersionedAggregateExporterSetter'):
        exporter.version = self.version

    def import_(self, exporter: 'IVersionedAggregateImporterGetter'):
        self.version = exporter.version


class IVersionedAggregateExporterSetter(metaclass=ABCMeta):

    @setterproperty
    @abstractmethod
    def version(self, value: int):
        raise NotImplementedError


class IVersionedAggregateImporterGetter(typing.Protocol, metaclass=ABCMeta):
    version: int
