from __future__ import annotations

import pickle

from blinker._utilities import Symbol


def test_symbols() -> None:
    foo = Symbol("foo")
    assert foo.name == "foo"
    assert foo is Symbol("foo")

    bar = Symbol("bar")
    assert foo is not bar
    assert foo != bar
    assert not foo == bar

    assert repr(foo) == "foo"


def test_pickled_symbols() -> None:
    foo = Symbol("foo")

    for _ in 0, 1, 2:
        roundtrip = pickle.loads(pickle.dumps(foo))
        assert roundtrip is foo
