import dataclasses
import typing
import uuid

from abc import ABCMeta, abstractmethod
from psycopg.errors import UniqueViolation

from ....domain.seedwork.aggregate import IDomainEventAccessor, EventMeta, PersistentDomainEvent, ConcurrentUpdate
from ..session import ISession
from ....application.seedwork.mediator import IMediator
from .event_insert_query import IEventInsertQuery

___all__ = ('EventStore', )


IPDE = typing.TypeVar('IPDE', bound=PersistentDomainEvent, covariant=True)


class EventStore(typing.Generic[IPDE], metaclass=ABCMeta):

    class Queries(dict):
        def register(self, event_type: typing.Type[PersistentDomainEvent], event_version: int):
            def do_register(query_cls: typing.Type[IEventInsertQuery]):
                self[(event_type.__name__, event_version)] = query_cls
                return query_cls

            return do_register

    queries = Queries()

    _session: ISession
    _stream_type: str
    mediator: IMediator

    def __init__(self, session: ISession):
        self._session = session

    async def _save(self, agg: IDomainEventAccessor[IPDE], event_meta: EventMeta):
        events = []
        pending_events = agg.pending_domain_events
        del agg.pending_domain_events

        causation_id = None
        for event in pending_events:
            event_id = uuid.uuid4()
            event_meta = dataclasses.replace(event_meta, event_id=event_id, causation_id=causation_id)
            causation_id = event_id
            event = dataclasses.replace(event, event_meta=event_meta)
            query = self._do_make_event_query(event)
            query.stream_type = self._stream_type
            try:
                await query.evaluate(self._session)
            except UniqueViolation as e:
                raise ConcurrentUpdate(query) from e
            events.append(event)

        for event in events:
            await self.mediator.publish(event, self._session)

    def _do_make_event_query(self, event: IPDE) -> IEventInsertQuery:
        return self.queries[(event.event_type, event.event_version)].make(event)
