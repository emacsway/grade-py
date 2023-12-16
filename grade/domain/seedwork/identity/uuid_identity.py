import uuid
from .identity import Identity

__all__ = ('UuidIdentity', )


class UuidIdentity(Identity[uuid.UUID]):
    pass
