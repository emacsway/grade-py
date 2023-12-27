from .identity import Identity

__all__ = ('StrIdentity', )


class StrIdentity(Identity[str]):

    def __init__(self, value: int):
        if value and not isinstance(value, str):
            raise ValueError("Type of StrIdentity value should be str, not %r", (value, ))
        super().__init__(value)
