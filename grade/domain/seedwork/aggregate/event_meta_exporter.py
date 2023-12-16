import datetime
import typing
import uuid

from ..utils import setterproperty
from .causal_dependency import CausalDependency
from .causal_dependency_exporter import CausalDependencyExporter
from .event_meta import IEventMetaExporterSetter

__all__ = ('EventMetaExporter', )


class EventMetaExporter(IEventMetaExporterSetter):

    def __init__(self):
        self.data: typing.Dict[str, typing.Any] = dict(
            causal_dependencies=list(),
        )

    @setterproperty
    def event_id(self, value: typing.Optional[uuid.UUID]):
        self.data['event_id'] = value

    @setterproperty
    def causation_id(self, value: typing.Optional[uuid.UUID]):
        self.data['causation_id'] = value

    @setterproperty
    def correlation_id(self, value: typing.Optional[uuid.UUID]):
        self.data['correlation_id'] = value

    @setterproperty
    def reason(self, value: typing.Optional[str]):
        self.data['reason'] = value

    @setterproperty
    def occurred_at(self, value: typing.Optional[datetime.datetime]):
        self.data['occurred_at'] = value

    def add_causal_dependency(self, value: CausalDependency):
        ex = CausalDependencyExporter()
        value.export(ex)
        self.data['causal_dependencies'].append(ex.data)
