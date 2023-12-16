import typing

from ..utils import setterproperty
from .causal_dependency import ICausalDependencyExporterSetter

__all__ = ('CausalDependencyExporter', )


class CausalDependencyExporter(ICausalDependencyExporterSetter):

    def __init__(self):
        self.data = dict()

    @setterproperty
    def aggregate_id(self, value: typing.Any):
        self.data['aggregate_id'] = value

    @setterproperty
    def aggregate_type(self, value: str):
        self.data['aggregate_type'] = value

    @setterproperty
    def aggregate_version(self, value: int):
        self.data['aggregate_version'] = value
