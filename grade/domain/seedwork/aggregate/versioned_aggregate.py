from abc import ABCMeta
from .interfaces import IVersionedAggregate

__all__ = ('VersionedAggregate', )


class VersionedAggregate(IVersionedAggregate, metaclass=ABCMeta):

    def __init__(self, version: int = 0, **kwargs):
        self.__version = version
        super().__init__(**kwargs)

    @property
    def version(self) -> int:
        return self.__version

    @version.setter
    def version(self, value: int):
        self.__version = value

    @property
    def next_version(self) -> int:
        self.__version += 1
        return self.__version
