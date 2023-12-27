import typing
import uuid
import dateutil.parser

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from ....domain.seedwork.aggregate import EventMeta, CausalDependency, IDomainEventLoader, PersistentDomainEvent
from ...seedwork.session import ISession
from .stream_id import StreamId

__all__ = ('EventGetQuery', 'IEventGetQuery', 'Row', )


@abstractmethod
class IEventGetQuery(metaclass=ABCMeta):
    async def evaluate(self, session: ISession) -> typing.Iterable[PersistentDomainEvent]:
        raise NotImplementedError


class EventGetQuery(IEventGetQuery, metaclass=ABCMeta):

    class Reconstitutors(dict):
        def register(self, event_type: typing.Type[PersistentDomainEvent], event_version: int):
            def do_register(reconstitutor: typing.Callable[['EventGetQuery', 'Row'], PersistentDomainEvent]):
                self[(event_type.__name__, event_version)] = reconstitutor
                return reconstitutor

            return do_register

    reconstitutors = Reconstitutors()

    """
    В запросе не нужны tenant_id, stream_type, stream_id, т.к. они уже известны и являются критериями выборки.
    """
    _sql = """
        SELECT
            stream_position, event_type, event_version, payload, metadata
        FROM
            event_log
        WHERE
            stream_type = %s AND stream_id = %s AND stream_position > %s
        ORDER BY
            tenant_id, stream_type, stream_id, stream_position
    """

    def __init__(self, stream_id: StreamId, since_position: int = 0):
        self._stream_id = stream_id
        self._since_position = since_position

    async def evaluate(self, session: ISession) -> typing.Iterable[PersistentDomainEvent]:
        async with session.connection.cursor() as acursor:
            params = [
                self._stream_id.stream_type, self._stream_id.stream_id, self._since_position
            ]
            await acursor.execute(self._sql, params)
            rows = await acursor.fetchall()
            past_events = tuple(self._reconstitute_event(Row(*row)) for row in rows)
            return past_events

    def _reconstitute_event(self, row: 'Row') -> PersistentDomainEvent:
        return self.reconstitutors[(row.event_type, row.event_version)](self, row)

    def _persistent_domain_event_kwargs(self, row: 'Row') -> typing.Dict:
        return dict(
            event_meta=self._reconstitute_event_meta(row.metadata),
            aggregate_version=row.aggregate_version,
        )

    def _reconstitute_event_meta(self, data: typing.Dict):
        """
        Meta can be customised, thus, allow to reload this method
        :param data:
        :return:
        """
        r = (lambda c, x: x and c(x))
        return EventMeta(
            event_id=r(uuid.UUID, data.get('event_id')),
            causation_id=r(uuid.UUID, data.get('causation_id')),
            correlation_id=r(uuid.UUID, data.get('correlation_id')),
            reason=data.get('reason'),
            occurred_at=r(dateutil.parser.isoparse, data.get('occurred_at')),
            causal_dependencies=tuple(map(self._reconstitute_causal_dependency,
                                          data.get('causal_dependencies', []))),
        )

    def _reconstitute_causal_dependency(self, data: typing.Dict):
        return CausalDependency(
            aggregate_id=data.get('aggregate_id'),
            aggregate_type=data.get('aggregate_type'),
            aggregate_version=data.get('aggregate_version'),
        )


@dataclass(frozen=True)
class Row:
    aggregate_version: int
    event_type: str
    event_version: int
    payload: typing.Dict
    metadata: typing.Dict
