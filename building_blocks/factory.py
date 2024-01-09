from functools import wraps

from .event_bus import IEventBus, InMemoryEventBus

__all__ = ('building_blocks_factory', 'BuildingBlocksFactory', 'amemo', )


def amemo(func):
    _cache = dict()

    @wraps(func)
    async def _deco(*args, **kwds):
        key = (tuple(args), tuple(kwds.items()))
        if key not in _cache:
            _cache[key] = await func(*args, **kwds)
        return _cache[key]
    return _deco


class BuildingBlocksFactory:

    @amemo
    async def make_in_memory_event_bus(self) -> IEventBus[str, dict]:
        return InMemoryEventBus[str, dict]()


building_blocks_factory = BuildingBlocksFactory()
