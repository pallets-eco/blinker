import pytest

from blinker import Signal


def test_temp_connection():
    sig = Signal()

    canary = []

    def receiver(sender):
        canary.append(sender)

    sig.send(1)
    with sig.connected_to(receiver):
        sig.send(2)
    sig.send(3)

    assert canary == [2]
    assert not sig.receivers


def test_temp_connection_for_sender():
    sig = Signal()

    canary = []

    def receiver(sender):
        canary.append(sender)

    with sig.connected_to(receiver, sender=2):
        sig.send(1)
        sig.send(2)

    assert canary == [2]
    assert not sig.receivers


class Failure(Exception):
    pass


class BaseFailure(BaseException):
    pass


@pytest.mark.parametrize("exc_type", [Failure, BaseFailure])
def test_temp_connection_failure(exc_type):
    sig = Signal()

    canary = []

    def receiver(sender):
        canary.append(sender)

    class Failure(Exception):
        pass

    with pytest.raises(exc_type):  # noqa: B908
        sig.send(1)
        with sig.connected_to(receiver):
            sig.send(2)
            raise exc_type
        sig.send(3)

    assert canary == [2]
    assert not sig.receivers
