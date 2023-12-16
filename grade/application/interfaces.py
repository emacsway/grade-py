import typing
from abc import ABCMeta, abstractmethod
from collections.abc import Callable, Awaitable

__all__ = ('ISession', )


class ISession(metaclass=ABCMeta):

    @abstractmethod
    async def __call__(self, func: Callable[['ISession'], Awaitable[typing.Any]]) -> typing.Any:
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> 'ISession':
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback) -> bool:
        raise NotImplementedError
