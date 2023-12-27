import typing
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from ..utils import setterproperty
from .domain_event import DomainEvent
from .event_meta import EventMeta

__all__ = ('PersistentDomainEvent', 'IPersistentDomainEventExporterSetter',)


@dataclass(frozen=True, kw_only=True)
class PersistentDomainEvent(DomainEvent):
    event_version: int = 1
    event_meta: typing.Optional[EventMeta] = None
    aggregate_version: int = 0
    # occurred_at: datetime.datetime = None  # для партиционирования?
    # Откуда это значение известно на уровне домена? Пусть останется в Meta.

    @property
    def event_type(self):
        return type(self).__name__

    def export(self, exporter: 'IPersistentDomainEventExporterSetter'):
        """
        Можно здесь использовать и рефлексию.
        Но я применил здесь классический подход по трем причинам:

        1. "programming in a language vs. programming into a language" -- Steve McConnell, Code Complete 2nd ed.
        Будет лучше придерживаться практик независимых от конкретного ЯП - это позволит
        легче переносить код на более производительный статически типизируемый ЯП.

        2. Рекомендация Greg Young:
        💬 This table represents the actual Event Log. There will be one entry per event in this table.
        The event itself is stored in the [Data] column.
        The event is stored using some form of serialization, for the rest of this discussion the mechanism
        will assumed to be built in serialization although the use of the memento pattern can be highly advantageous.
        -- "`CQRS Documents by Greg Young <https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf>`__"

        3. Это не так страшно, т.к. ввод символов с клавиатуры не оказывает существенного влияния на темпы разработки,
        поскольку занимает не более 10% от времени конструирования кода.
        При этом вероятность возникновения ошибки тоже минимальна, т.к. легко отлавливается статическим анализатором кода.

        В перспективе весь код будет генерироваться по EventStorming диаграммам и будет применяться code generation,
        см. главу "Metadata Mapping" книги "Patterns of Enterprise Application Architecture" by Martin Fowler

        См. также:
        https://dckms.github.io/system-architecture/emacsway/it/ddd/grade/domain/shotgun-surgery.html
        """
        exporter.event_type = self.event_type
        exporter.event_version = self.event_version
        exporter.event_meta = self.event_meta
        exporter.aggregate_version = self.aggregate_version


class IPersistentDomainEventExporterSetter(metaclass=ABCMeta):
    @setterproperty
    @abstractmethod
    def event_type(self, value: str):
        raise NotImplementedError

    @setterproperty
    @abstractmethod
    def event_version(self, value: int):
        raise NotImplementedError

    @setterproperty
    @abstractmethod
    def event_meta(self, meta: EventMeta):
        raise NotImplementedError

    @setterproperty
    @abstractmethod
    def aggregate_version(self, value: int):
        raise NotImplementedError
