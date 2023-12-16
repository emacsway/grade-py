import typing
from abc import ABCMeta, abstractmethod

from ..utils import setterproperty
from .event_meta import EventMeta
from .event_meta_exporter import EventMetaExporter
from .persistent_domain_event import IPersistentDomainEventExporterSetter

__all__ = ('PersistentDomainEventExporter', )


class PersistentDomainEventExporter(IPersistentDomainEventExporterSetter):

    def __init__(self):
        self.data = dict()

    @setterproperty
    def event_type(self, value: str):
        self.data['event_type'] = value

    @setterproperty
    def event_version(self, value: int):
        self.data['event_version'] = value

    @setterproperty
    def event_meta(self, meta: EventMeta):
        exporter = EventMetaExporter()
        meta.export(exporter)
        self.data['event_meta'] = meta

    @setterproperty
    def aggregate_version(self, value: int):
        self.data['aggregate_version'] = value
