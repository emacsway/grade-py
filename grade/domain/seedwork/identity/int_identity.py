from .identity import Identity

__all__ = ('IntIdentity', )


class IntIdentity(Identity[int]):

    def __init__(self, value: int):
        if value and not isinstance(value, int):
            raise ValueError("Type of IntIdentity value should be int, not %r", (value, ))
        super().__init__(value)
