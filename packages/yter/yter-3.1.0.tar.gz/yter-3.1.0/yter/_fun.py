"""Functions for getting data from iterators for yter"""

import sys
import itertools
import collections


if sys.version_info[0] < 3:
    _ignoreTypes = (basestring, BaseException)  # pylint: disable=undefined-variable
else:
    _ignoreTypes = (str, bytes)


def yany(y, key=None, empty=False):
    """Extended version of the builtin any, test if any values are true.

    Unlike the builtin `any` method, this will return the last value iterated
    before ending. This will short circuit or exit early when a correct answer
    is found.

    A simple explanation is that this will be the first true value or the final
    false value of the interator. This is the same as calling the logical or
    operator on all the iterated values.

    The `key` is an optional function that will be called on each value in
    iterator. The return of that function will be used to test if the value is
    true or false.

    If the iterator is empty this will return the empty argument. This defaults
    to False, the same as the built in `any`.

    # Examples

    >>> yter.yany([0, False, 1.1, ""])
    1.1
    >>> yter.yany([2.2, 3.3, 4.0, 5.5], key=float.is_integer)
    4.0
    >>> yter.yany([])
    False

    # Implementation details

    This will advance the given iterator until the first non-true value
    is found, which will not always consume the entire iterator. This will
    generally be faster than something like `itertools.takewhile` but
    never as fast as the builtin `any` method.
    
    """
    val = empty
    if key:
        for val in y:
            if key(val):
                return val
    else:
        for val in y:
            if val:
                return val
    return val


def yall(y, key=None, empty=True):
    """Extended version of the builtin all, test if all values are true.

    Unlike the builtin `all` method, this will return the last value iterated
    before ending. This will short circuit or exit early when a correct answer
    is found.

    A simple explanation is that this will be the final true value or the first
    false value of the interator. This is the same as calling the logical and
    operator on all the iterated values.

    The `key` is an optional function that will be called on each value in
    iterator. The return of that function will be used to test if the value is
    true or false.

    If the iterable is empty this will return the empty argument. This defaults
    to True, the same as the built in `all`.

    # Examples

    >>> yter.yall([0, False, 1.1, ""])
    0
    >>> yter.yall([2.0, 3.0, 4.4, 5.0], key=float.is_integer)
    4.4
    >>> yter.yall([])
    True

    # Implementation details

    This will advance the given iterator until the first non-true value
    is found, which will not always consume the entire iterator. This will
    generally be faster than something like `itertools.takewhile` but
    never as fast as the builtin `all` method.

    """
    val = empty
    if key:
        for val in y:
            if not key(val):
                return val
    else:
        for val in y:
            if not val:
                return val
    return val


def first(y, empty=None):
    """Get the final value from an iterator.

    This will get the first value from an iterable object. This is an
    improvement over the builtin `next` because it works any iterable object,
    not just an iterator. If given an iterator it will be advanced by a single
    value.

    If the iterable contains no values then the `empty` argument is returned.

    This is useful when trying to get any value out of a container that
    may not provide integer indexing.

    This is similar to `head` which returns a container of the first
    values in an iterator, instead of just the first value.

    # Examples

    >>> values = {"car"}
    >>> yter.first(values)
    "car"

    # Implementation details

    This really is just a wrapper around `next` to allow it to work with 
    containers and iterators.
    
    """
    return next(iter(y), empty)


def last(y, empty=None):
    """Get the final value from an iterator.

    This will get the final value from an iterable object. If the iterable 
    contains no values then the `empty` argument is returned.

    # Examples

    >>> yter.last("abcdef")
    'f'
    >>> yter.last(range(10_000_000))
    9999999

    # Implementation details

    This will check if the builtin `reversed` function can be used. If so it will
    get the first value from the iterator. Otherwise the iterable will be
    passed through a single item deque.

    """
    try:
        ry = reversed(y)
    except TypeError:
        buf = collections.deque(y, maxlen=1)
        return buf[0] if buf else empty
    else:
        return next(ry, empty)


def head(y, count, container=list):
    """Get the first values from an iterator.

    This will be a list of values no larger than `count`. This is similar to
    `yter.first` but returns a container of values, instead of just the first.

    The container argument defaults to a list, but any type of container
    can be used, that accepts an iterable argument.
    
    # Examples

    >>> yter.head(range(10_000_000), 3)
    [0, 1, 2]
    >>> yter.head("abcdef", 3, container=tuple)
    ('a', 'b', 'c')

    # Implementation details

    The iterator will always be advanced by the given ``count``.

    """
    return container(itertools.islice(y, count))


def tail(y, count, container=list):
    """Get the last values from an iterator.

    This will be a new list of values no larger than `count`.

    If the iterable object can be `reversed` then a more efficient algorithm is
    used. Otherwise this will always finish the iterable object.

    The container argument defaults to a list, but any type of container
    can be used, that accepts an iterable argument.

    # Examples

    >>> yter.tail(range(10_000_000), 3)
    [9999997, 9999998, 9999999]
    >>> yter.tail("abcdef", 3, container=tuple)
    ('d', 'e', 'f')

    # Implementation details

    If the iterator or container supports the `reversed` builtin then this
    will only get the first values from that list. Otherwise the iterator
    will be fully advanced to get all the values.

    """
    try:
        rev = reversed(y)
    except TypeError:
        return container(collections.deque(y,  maxlen=count))

    items = list(itertools.islice(rev, count))
    if container is list:
        items.reverse()
    else:
        items = container(reversed(items))
    return items


def ylen(y):
    """Complete an iterator and get number of iterations.

    Get all the values from an iterator and return the number of values it
    contained. An empty iterable will return 0.

    The values from the iterator are discarded.

    # Examples

    >>> yter.ylen("abcdef")
    6
    >>> yter.ylen(zip("Hello", "Will"))
    4

    # Implementation details

    The given iterator will be fully used when complete. If the given object
    implements the `len` builtin, it will simply use that. Otherwise this 
    will advance the iterator in increments of about 4000 items while tallying
    the number of items.
    
    """
    try:
        return len(y)
    except TypeError:
        pass
    y = iter(y)
    span = l = 4000
    buf = collections.deque(maxlen=span)
    count = 0
    while l == span:
        buf.clear()
        buf.extend(itertools.islice(y, span))
        l = len(buf)
        count += l
    return count


def minmax(y, key=None, empty=None):
    """Find the minimum and maximum values from an iterable.

    This will always return a tuple of two values. If the iterable contains no
    values it the tuple will contain two values of the `empty` argument.

    The minimum and maximum preserve order. So the first value that compares
    equal will be considered the minimum and the last equal value is considered
    the maximum. If you sorted the iterable, this is the same as the first and
    last values from that list.

    The `key` is an optional function that will be called on each value in
    iterator. The return of that function will be used to sort the values from
    the iterator.

    # Examples

    >>> yter.minmax([1, 2, 3, 4, 5])
    (1, 5)
    >>> yter.minmax(["first", "second", "third], key=len)
    ('first', 'second')
    >>> yter.minmax({}, empty=0.0)
    (0.0, 0.0)

    # Implementation details

    This should be faster than calling both `min` and `max` on the same
    container. Which is only possible when using containers, not
    iterators.
    
    """
    y = iter(y)
    try:
        minval = maxval = next(y)
    except StopIteration:
        return (empty, empty)
    minkey = maxkey = key(minval) if key else minval

    for val in y:
        curkey = key(val) if key else val
        if curkey < minkey:
            minval = val
            minkey = curkey
        elif curkey >= maxkey:
            maxval = val
            maxkey = curkey
    return (minval, maxval)


def isiter(y, ignore=_ignoreTypes):
    """Test if an object is iterable, but not a string type.

    Test if an object is an iterator or is iterable itself. By default this does
    not return True for string objects. Python 2 will also ignore exception
    types.

    The `ignore` argument defaults to a list of string types that are not
    considered iterable. This can be used to also exclude things like
    dictionaries or named tuples. It will be used as an argument to
    `isinstance`. If ignore is set to None, it will be ignored.

    # Examples

    >>> yter.isiter([1, 2, 3])
    True
    >>> yter.isiter({"a": 1, "b": 2}.items())
    True
    >>> yter.isiter("abc")
    False
    >>> yter.isiter(ValueError("Wrong Value"))
    False

    """
    if ignore and isinstance(y, ignore):
        return False
    try:
        iter(y)
        return True
    except TypeError:
        return False


def uniter(y, container=list):
    """Ensure any iterable is a real container.

    If the value is already a container, like a list or tuple, then return the
    original value. Otherwise the value must be an iterator that will be copied
    into a new container of the given type. If the value already appears
    to be a container and not an iterator, then it will be returned unconverted.

    This gives an efficient way to call `len` or repeat an iterator without
    duplicating data already in a container.

    # Examples

    >>> yter.uniter([1, 2, 3])
    [1, 2, 3]
    >>> yter.uniter(range(5, 8))
    [5, 6, 7]
    >>> yter.uniter("abc", container=tuple)
    ('a', 'b', 'c')
    >>> yter.uniter({"a": 1, "b": 2}.items())

    """
    if iter(y) is not y:
        return y
    return container(y)


def repeatable(y):
    """Efficient lazy copy of non sequence data.

    If the value is already a sequence, that will be returned with no changes.
    Otherwise this will wrap the results in an iterator that lazily copies all
    values for repeated use.

    This allows efficient use of containers when no copy is needed to iterate
    the data multiple times.

    This is slightly less efficient than `yter.uniter`, but if only iterating a
    portion of the data, this will not require a full copy.

    Be aware that repeatable is still an iterable, and calls like len()
    will often not work, depending on the iterable argument.

    # Examples

    >>> iterable = zip("abc", "123")
    >>> repeat = yter.repeatable(iterable)
    >>> tuple(repeat), tuple(repeat)
    ((('a', '1'), ('b', '2'), ('c', '3')), (('a', '1'), ('b', '2'), ('c', '3')))

    """
    yiter = iter(y)
    if yiter is not y:
        # Object does not need a separate iterator
        return y
    return _Repeat(y)


class _Repeat(object):
    """Iterator that can be reused any number of times"""

    def __init__(self, it):
        self.__tee1, self.__tee2 = itertools.tee(it)

    def __iter__(self):
        return self.__tee2.__copy__()
