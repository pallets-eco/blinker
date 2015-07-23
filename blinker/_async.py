import asyncio

from blinker.base import Signal


try:
    schedule = asyncio.ensure_future
except AttributeError:
    schedule = asyncio.async


@asyncio.coroutine
def _wrap_plain_value(value):
    """Pass through a coroutine *value* or wrap a plain value."""
    if asyncio.iscoroutine(value):
        value = yield from value
    return value


def send_async(self, *sender, **kwargs):
    return [(receiver, schedule(_wrap_plain_value(value)))
            for receiver, value
            in self.send(*sender, **kwargs)]


send_async.__doc__ = Signal.send_async.__doc__
Signal.send_async = send_async

