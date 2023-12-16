import typing
from abc import ABCMeta, abstractmethod


__all__ = ('IEqualOperand', )


class IEqualOperand(typing.Protocol, metaclass=ABCMeta):

    @abstractmethod
    def __eq__(self, other: 'IEqualOperand'):
        raise NotImplementedError
