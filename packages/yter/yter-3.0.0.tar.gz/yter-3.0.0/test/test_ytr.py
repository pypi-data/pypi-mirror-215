import itertools
import yter


def test_call():
    assert tuple(yter.call((0, 1, lambda: 2))) == (0, 1, 2)
    assert tuple(yter.call(())) == ()


def test_percent():
    assert tuple(yter.percent((0, 1, 2), 0.5)) == (0, 2)

    numbers = tuple(range(100))
    assert tuple(yter.percent(numbers, 1)) == numbers
    assert tuple(yter.percent(numbers, 1.1)) == numbers
    assert tuple(yter.percent(numbers, 5.5)) == numbers

    assert len(tuple(yter.percent(numbers, 0))) == 0
    assert len(tuple(yter.percent(numbers, 0.0))) == 0
    assert len(tuple(yter.percent(numbers, 0.01))) == 1
    assert len(tuple(yter.percent(numbers, 0.11))) == 11
    assert len(tuple(yter.percent(numbers, .47))) == 47


def test_flat():
    assert tuple(yter.flat(((0, 1), (2,)))) == (0, 1, 2)


def test_chunk():
    assert tuple(map(tuple, yter.chunk((0, 1, 2), 2))) == ((0, 1), (2,))
    assert tuple(map(tuple, yter.chunk(itertools.chain((0, 1, 2)), 2))) == ((0, 1), (2,))


def test_key():
    assert tuple(yter.key(("one", "two", "three", "four"), len)) == (
        (3, "one"), (3, "two"), (5, "three"), (4, "four"))


def test_choose():
    numiter = iter([0, 1, 2, 3, 0])
    a, b = yter.choose(numiter)
    assert tuple(a) == (1, 2, 3)
    assert tuple(b) == (0, 0)
    a, b = yter.choose(numiter)
    assert tuple(a) == ()
    assert tuple(b) == ()

    text = "Once Apon A Time"
    a, b = yter.choose(text, str.islower)
    assert "".join(a) == "nceponime"
    assert "".join(b) == "O A A T"


def test_unique():
    assert tuple(yter.unique((1, 1, 2, 3, 1))) == (1, 2, 3)
    assert tuple(yter.unique((1, 1, 2, 3, 1), key=lambda k: 0)) == (1,)


def test_duplicates():
    assert tuple(yter.duplicates((1, 1, 2, 3, 1))) == (1, 1)
    assert tuple(yter.duplicates((1, 1, 2, 3, 1), key=lambda k: 0)) == (1, 2, 3, 1)


def test_recurse():
    friends = {
       "alice": ["bob", "terry"], 
       "bob": ["edward", "dave"],
       "dave": ["alice", "bob"],
       "edward": ["dave", "alice"],
       "gary": ["dave", "bob"],
    }
    data = list(yter.recurse(["alice"], friends.get))
    assert data == ['alice', 'bob', 'terry', 'edward', 'dave']