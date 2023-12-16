import typing
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from ..utils import setterproperty

__all__ = ('CausalDependency', 'ICausalDependencyExporterSetter', )


@dataclass(frozen=True)
class CausalDependency:
    aggregate_id: typing.Any
    aggregate_type: str
    aggregate_version: int

    def export(self, exporter: 'ICausalDependencyExporterSetter'):
        exporter.aggregate_id = self.aggregate_id
        exporter.aggregate_type = self.aggregate_type
        exporter.aggregate_version = self.aggregate_version


class ICausalDependencyExporterSetter(metaclass=ABCMeta):

    @setterproperty
    @abstractmethod
    def aggregate_id(self, value: typing.Any):
        raise NotImplementedError

    @setterproperty
    @abstractmethod
    def aggregate_type(self, value: str):
        raise NotImplementedError

    @setterproperty
    @abstractmethod
    def aggregate_version(self, value: int):
        raise NotImplementedError
