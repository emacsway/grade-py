import datetime
import typing
import uuid

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from ..utils import setterproperty
from .causal_dependency import CausalDependency

__all__ = ('EventMeta', 'IEventMetaExporterSetter', )


@dataclass(frozen=True)
class EventMeta:
    event_id: typing.Optional[uuid.UUID] = None
    causation_id: typing.Optional[uuid.UUID] = None
    correlation_id: typing.Optional[uuid.UUID] = None
    reason: typing.Optional[str] = None
    occurred_at: typing.Optional[datetime.datetime] = None
    causal_dependencies: typing.Tuple[CausalDependency] = tuple()

    def export(self, exporter: 'IEventMetaExporterSetter'):
        exporter.event_id = self.event_id
        exporter.causation_id = self.causation_id
        exporter.correlation_id = self.correlation_id
        exporter.reason = self.reason
        exporter.occurred_at = self.occurred_at
        for causal_dependency in self.causal_dependencies:
            exporter.add_causal_dependency(causal_dependency)


class IEventMetaExporterSetter(metaclass=ABCMeta):

    @setterproperty
    @abstractmethod
    def event_id(self, value: typing.Optional[uuid.UUID]):
        raise NotImplementedError

    @setterproperty
    @abstractmethod
    def causation_id(self, value: typing.Optional[uuid.UUID]):
        raise NotImplementedError

    @setterproperty
    @abstractmethod
    def correlation_id(self, value: typing.Optional[uuid.UUID]):
        raise NotImplementedError

    @setterproperty
    @abstractmethod
    def reason(self, value: typing.Optional[str]):
        raise NotImplementedError

    @setterproperty
    @abstractmethod
    def occurred_at(self, value: typing.Optional[datetime.datetime]):
        raise NotImplementedError

    @abstractmethod
    def add_causal_dependency(self, value: CausalDependency):
        raise NotImplementedError
