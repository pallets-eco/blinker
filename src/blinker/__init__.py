from __future__ import annotations

import typing as t

from blinker.base import ANY
from blinker.base import NamedSignal
from blinker.base import Namespace
from blinker.base import Signal
from blinker.base import signal
from blinker.base import WeakNamespace

__all__ = [
    "ANY",
    "NamedSignal",
    "Namespace",
    "Signal",
    "WeakNamespace",
    "signal",
]


def __getattr__(name: str) -> t.Any:
    import warnings

    if name == "__version__":
        import importlib.metadata

        warnings.warn(
            "The '__version__' attribute is deprecated and will be removed in"
            " Blinker 1.9.0. Use feature detection or"
            " 'importlib.metadata.version(\"blinker\")' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return importlib.metadata.version("blinker")

    if name == "receiver_connected":
        from .base import _receiver_connected

        warnings.warn(
            "The global 'receiver_connected' signal is deprecated and will be"
            " removed in Blinker 1.9. Use 'Signal.receiver_connected' and"
            " 'Signal.receiver_disconnected' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _receiver_connected

    raise AttributeError(name)
