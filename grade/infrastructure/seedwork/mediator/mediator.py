import typing
import collections
from ....application.seedwork.mediator import (
    IMediator, ICommandHandler, IEventHandler
)
from ....domain.seedwork.disposable import IDisposable, Disposable

__all__ = ('Mediator',)

ISession = typing.TypeVar('ISession', covariant=True)
ICommand = typing.TypeVar('ICommand', covariant=True)
IEvent = typing.TypeVar('IEvent', covariant=True)


class Mediator(typing.Generic[ICommand, IEvent, ISession], IMediator[ICommand, IEvent, ISession]):
    def __init__(self):
        self._subscribers = collections.defaultdict(list)
        self._handlers = dict()

    async def send(self, command: ICommand):
        if type(command) in self._handlers:
            return await self._handlers[type(command)](command)

    async def register(self, command_type: typing.Type[ICommand], handler: ICommandHandler) -> IDisposable:
        self._handlers[command_type] = handler

        async def callback():
            await self.unregister(command_type)

        return Disposable(callback)

    async def unregister(self, command_type: typing.Type[ICommand]):
        self._handlers.pop(command_type)

    async def publish(self, event: IEvent, session: ISession):
        for handler in self._subscribers[type(event)]:
            await handler(event, session)

    async def subscribe(self, event_type: typing.Type[IEvent], handler: IEventHandler) -> IDisposable:
        self._subscribers[event_type].append(handler)

        async def callback():
            await self.unsubscribe(event_type, handler)

        return Disposable(callback)

    async def unsubscribe(self, event_type: typing.Type[IEvent], handler: IEventHandler):
        self._subscribers[event_type].remove(handler)
