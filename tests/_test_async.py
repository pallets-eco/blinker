import asyncio

import blinker


def test_send_async():
    calls = []

    @asyncio.coroutine
    def receiver_a(sender):
        calls.append(receiver_a)
        return 'value a'

    @asyncio.coroutine
    def receiver_b(sender):
        calls.append(receiver_b)
        return 'value b'

    def receiver_c(sender):
        calls.append(receiver_c)
        return 'value c'

    sig = blinker.Signal()
    sig.connect(receiver_a)
    sig.connect(receiver_b)
    sig.connect(receiver_c)

    @asyncio.coroutine
    def collect():
        return sig.send_async()

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(collect())

    expected = {
        receiver_a: 'value a',
        receiver_b: 'value b',
        receiver_c: 'value c',
        }

    assert set(calls) == set(expected.keys())
    collected_results = {v.result() for r, v in results}
    assert collected_results == set(expected.values())
