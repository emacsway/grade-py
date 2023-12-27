import uuid
from .identity import Identity

__all__ = ('UuidIdentity', )


class UuidIdentity(Identity[uuid.UUID]):

    def __init__(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("Type of UuidIdentity value should be UUID, not %r", (value, ))
        super().__init__(value)
