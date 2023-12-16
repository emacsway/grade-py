import typing
from abc import ABCMeta, abstractmethod
from psycopg import AsyncConnection

from ....application.interfaces import ISession as _ISession
from ....domain.seedwork.aggregate import IHashable


__all__ = ('ISession', 'IIdentityMap', 'IIdentityKey', 'IModel', )


IIdentityKey = IHashable
IModel = typing.Any


class IIdentityMap(metaclass=ABCMeta):
    @abstractmethod
    def get(self, key: IIdentityKey) -> typing.Optional[IModel]:
        raise NotImplementedError

    @abstractmethod
    def has(self, key: IIdentityKey) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add(self, key: IIdentityKey, obj: IModel):
        raise NotImplementedError

    @abstractmethod
    def remove(self, key: IIdentityKey):
        raise NotImplementedError

    @abstractmethod
    def clear(self):
        raise NotImplementedError


class ISession(_ISession, metaclass=ABCMeta):

    @property
    @abstractmethod
    def connection(self) -> AsyncConnection[typing.Any]:
        raise NotImplementedError

    @property
    @abstractmethod
    def identity_map(self) -> IIdentityMap:
        raise NotImplementedError
