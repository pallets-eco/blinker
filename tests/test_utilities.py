import pickle

from blinker._utilities import symbol
from blinker._utilities import merge_lists_unique


def test_symbols():
    foo = symbol("foo")
    assert foo.name == "foo"
    assert foo is symbol("foo")

    bar = symbol("bar")
    assert foo is not bar
    assert foo != bar
    assert not foo == bar

    assert repr(foo) == "foo"


def test_pickled_symbols():
    foo = symbol("foo")

    for _ in 0, 1, 2:
        roundtrip = pickle.loads(pickle.dumps(foo))
        assert roundtrip is foo


def test_merge_lists_unique():
    assert merge_lists_unique([123]) == [123]
    assert merge_lists_unique([123], [456]) == [123, 456]
    assert merge_lists_unique([123, 456], [456]) == [123, 456]
    assert merge_lists_unique([123, 456], [456, 123]) == [123, 456]
