from __future__ import annotations

import typing as t
from weakref import ref

from blinker._saferef import BoundMethodWeakref

if t.TYPE_CHECKING:
    pass

IdentityType = t.Union[t.Tuple[int, int], str, int]


class _symbol:
    def __init__(self, name: str) -> None:
        """Construct a new named symbol."""
        self.__name__ = name
        self.name = name

    def __reduce__(self) -> tuple[t.Any, ...]:
        return symbol, (self.name,)

    def __repr__(self) -> str:
        return self.name


_symbol.__name__ = "symbol"


class symbol:
    """A constant symbol.

    >>> symbol('foo') is symbol('foo')
    True
    >>> symbol('foo')
    foo

    A slight refinement of the MAGICCOOKIE=object() pattern.  The primary
    advantage of symbol() is its repr().  They are also singletons.

    Repeated calls of symbol('name') will all return the same instance.

    """

    symbols: dict[str, _symbol] = {}
    name: str

    def __new__(cls, name: str) -> _symbol:  # type: ignore[misc]
        try:
            return cls.symbols[name]
        except KeyError:
            return cls.symbols.setdefault(name, _symbol(name))


def hashable_identity(obj: object) -> IdentityType:
    if hasattr(obj, "__func__"):
        return (id(obj.__func__), id(obj.__self__))  # type: ignore[attr-defined]
    elif hasattr(obj, "im_func"):
        return (id(obj.im_func), id(obj.im_self))  # type: ignore[attr-defined]
    elif isinstance(obj, (int, str)):
        return obj
    else:
        return id(obj)


WeakTypes = (ref, BoundMethodWeakref)


class annotatable_weakref(ref):  # type: ignore[type-arg]
    """A weakref.ref that supports custom instance attributes."""

    receiver_id: IdentityType | None
    sender_id: IdentityType | None


def reference(
    object: t.Any,
    callback: t.Callable[[annotatable_weakref], None] | None = None,
    **annotations: t.Any,
) -> annotatable_weakref:
    """Return an annotated weak ref."""
    if callable(object):
        weak = callable_reference(object, callback)
    else:
        weak = annotatable_weakref(object, callback)  # type: ignore[arg-type]
    for key, value in annotations.items():
        setattr(weak, key, value)
    return weak


def callable_reference(
    object: t.Callable[..., t.Any],
    callback: t.Callable[[annotatable_weakref], None] | None = None,
) -> annotatable_weakref:
    """Return an annotated weak ref, supporting bound instance methods."""
    if hasattr(object, "im_self") and object.im_self is not None:
        return BoundMethodWeakref(target=object, on_delete=callback)  # type: ignore[arg-type, return-value]
    elif hasattr(object, "__self__") and object.__self__ is not None:
        return BoundMethodWeakref(target=object, on_delete=callback)  # type: ignore[arg-type, return-value]
    return annotatable_weakref(object, callback)  # type: ignore[arg-type]


class lazy_property:
    """A @property that is only evaluated once."""

    def __init__(self, deferred: t.Callable[[t.Any], t.Any]) -> None:
        self._deferred = deferred
        self.__doc__ = deferred.__doc__

    def __get__(self, obj: t.Any | None, cls: type[t.Any]) -> t.Any:
        if obj is None:
            return self
        value = self._deferred(obj)
        setattr(obj, self._deferred.__name__, value)
        return value
