from __future__ import with_statement

from blinker import Signal


def test_temp_connection():
    sig = Signal()

    canary = []
    receiver = lambda sender: canary.append(sender)

    sig.send(1)
    with sig.connected_to(receiver):
        sig.send(2)
    sig.send(3)

    assert canary == [2]
    assert not sig.receivers


def test_temp_connection_for_sender():
    sig = Signal()

    canary = []
    receiver = lambda sender: canary.append(sender)

    with sig.connected_to(receiver, sender=2):
        sig.send(1)
        sig.send(2)

    assert canary == [2]
    assert not sig.receivers


def test_temp_connection_failure():
    sig = Signal()

    canary = []
    receiver = lambda sender: canary.append(sender)

    class Failure(Exception):
        pass

    try:
        sig.send(1)
        with sig.connected_to(receiver):
            sig.send(2)
            raise Failure
        sig.send(3)
    except Failure:
        pass
    else:
        raise AssertionError("Context manager did not propagate.")

    assert canary == [2]
    assert not sig.receivers
