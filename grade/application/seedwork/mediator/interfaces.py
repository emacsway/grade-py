import typing
from abc import ABCMeta, abstractmethod
from collections.abc import Callable, Awaitable

from ....domain.seedwork.disposable import IDisposable

__all__ = ('IMediator', 'ICommandHandler', 'IEventHandler', )


ISession = typing.TypeVar('ISession', covariant=True)
ICommand = typing.TypeVar('ICommand', covariant=True)
ICommandHandler = Callable[[ICommand], Awaitable[typing.Any]]


IEvent = typing.TypeVar('IEvent', covariant=True)
IEventHandler = Callable[[IEvent], Awaitable[None]]


class IMediator(typing.Generic[ICommand, IEvent, ISession], metaclass=ABCMeta):

    @abstractmethod
    async def send(self, command: ICommand):
        raise NotImplementedError

    @abstractmethod
    async def register(self, command_type: typing.Type[ICommand], handler: ICommandHandler) -> IDisposable:
        raise NotImplementedError

    @abstractmethod
    async def unregister(self, command_type: typing.Type[ICommand]):
        raise NotImplementedError

    @abstractmethod
    async def publish(self, event: IEvent, session: ISession):
        raise NotImplementedError

    @abstractmethod
    async def subscribe(self, event_type: typing.Type[IEvent], handler: IEventHandler) -> IDisposable:
        raise NotImplementedError

    @abstractmethod
    async def unsubscribe(self, event_type: typing.Type[IEvent], handler: IEventHandler):
        raise NotImplementedError
