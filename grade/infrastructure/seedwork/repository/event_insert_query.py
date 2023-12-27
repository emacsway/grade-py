import typing
import json

from abc import ABCMeta, abstractmethod

from ....domain.seedwork.utils import setterproperty
from ....domain.seedwork.aggregate import EventMeta, EventMetaExporter, IPersistentDomainEventExporterSetter
from ...seedwork.session import ISession
from .json import JSONEncoder

__all__ = ('EventInsertQuery', 'IEventInsertQuery')


@abstractmethod
class IEventInsertQuery(IPersistentDomainEventExporterSetter, metaclass=ABCMeta):
    async def evaluate(self, session: ISession) -> None:
        raise NotImplementedError


class EventInsertQuery(IEventInsertQuery, metaclass=ABCMeta):
    # TODO: add occurred_at column to table for partitioning reason? created_at with default = NOW()
    _sql = """
        INSERT INTO event_log
        (tenant_id, stream_type, stream_id, stream_position, event_type, event_version, payload, metadata)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    def __init__(self):
        self.data = dict()
        self._params: typing.List[typing.Any] = [None] * 8
        self._metadata = dict()

    @setterproperty
    def tenant_id(self, value: str):
        self._params[0] = value

    @setterproperty
    def stream_type(self, value: str):
        self._params[1] = value

    @setterproperty
    def stream_id(self, value: int):
        self._params[2] = value

    @setterproperty
    def aggregate_version(self, value: int):
        self._params[3] = value

    @setterproperty
    def event_type(self, value: str):
        self._params[4] = value

    @setterproperty
    def event_version(self, value: int):
        self._params[5] = value

    @setterproperty
    def event_meta(self, meta: EventMeta):
        exporter = EventMetaExporter()
        meta.export(exporter)
        self._params[7] = self._encode(exporter.data)

    async def evaluate(self, session: ISession):
        self._params[6] = self._encode(self.data)
        async with session.connection.cursor() as acursor:
            await acursor.execute(self._sql, self._params)

    @staticmethod
    def _encode(obj):
        return json.dumps(obj, cls=JSONEncoder)
