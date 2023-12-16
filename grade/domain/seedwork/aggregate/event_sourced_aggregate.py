import typing
import dataclasses
from abc import ABCMeta

from .interfaces import IEventSourcedAggregate
from .eventive_entity import EventiveEntity
from .versioned_aggregate import VersionedAggregate

__all__ = ('EventSourcedAggregate', )

IPDE = typing.TypeVar('IPDE', covariant=True)


class EventSourcedAggregate(typing.Generic[IPDE], EventiveEntity[IPDE], VersionedAggregate,
                            IEventSourcedAggregate[IPDE], metaclass=ABCMeta):
    __handlers = dict()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __init_subclass__(cls):
        cls._register_handlers()

    @classmethod
    def _register_handlers(cls):
        pass

    @classmethod
    def _add_handler(cls, event_type: typing.Type[IPDE], handler: typing.Callable[[IPDE], None]):
        cls.__handlers[event_type] = handler

    def load_from(self, past_events: typing.Iterable[IPDE]):
        for event in past_events:
            self.version = event.aggregate_version
            self.__handlers[type(event)](self, event)

    def _update(self, event: IPDE):
        event = dataclasses.replace(event, aggregate_version=self.next_version)
        self.__handlers[type(event)](self, event)
        self._add_domain_event(event)
