import dataclasses
import typing

from abc import ABCMeta, abstractmethod
from psycopg.errors import UniqueViolation

from ....domain.seedwork.aggregate import IDomainEventAccessor, EventMeta, PersistentDomainEvent, ConcurrentUpdate
from ..session import ISession
from ....application.seedwork.mediator import IMediator
from .event_insert_query import EventInsertQuery

___all__ = ('EventStore', )


IPDE = typing.TypeVar('IPDE', bound=PersistentDomainEvent, covariant=True)


class EventStore(typing.Generic[IPDE], metaclass=ABCMeta):
    _session: ISession
    _stream_type: str
    mediator: IMediator

    def __init__(self, session: ISession):
        self._session = session

    async def _save(self, agg: IDomainEventAccessor[IPDE], event_meta: EventMeta):
        events = []
        for event in agg.pending_domain_events:
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

        del agg.pending_domain_events

    @abstractmethod
    def _do_make_event_query(self, event: IPDE) -> EventInsertQuery:
        raise NotImplementedError
