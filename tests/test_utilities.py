import pickle

from blinker._utilities import symbol


def test_symbols():
    foo = symbol('foo')
    assert foo.name == 'foo'
    assert foo is symbol('foo')

    bar = symbol('bar')
    assert foo is not bar
    assert foo != bar
    assert not foo == bar

    assert repr(foo) == 'foo'


def test_pickled_symbols():
    foo = symbol('foo')

    for protocol in 0, 1, 2:
        roundtrip = pickle.loads(pickle.dumps(foo))
        assert roundtrip is foo
