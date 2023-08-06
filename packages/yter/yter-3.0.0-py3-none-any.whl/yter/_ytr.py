"""Iterators that wrap iterators for yter"""

import itertools


def call(y, *args, **kwargs):
    """Iterator that works with mixed callable types.

    Iterate over all the values from the input iterator. If one of the values is
    a callable object it will be called and its return will be the value
    instead.

    This is mostly useful when iterating callables that may by mixed with
    predefined values, which can often be ``None`` or other placeholder values.
    It is the same as ``v(*args,**kargs) if callable(v) else v for v in y``

    The `args` and `kwargs` arguments will be passed to any callable values in
    the iterator.

    # Examples

    >>> callbacks = [len, str.upper, 5.5]
    >>> list(yter.call(callbacks, "hello"))
    [5, 'HELLO', 5.5]

    """
    _callable = callable  # Local cache
    for val in y:
        if _callable(val):
            val = val(*args, **kwargs)
        yield val


def percent(y, pct):
    """Iterator that skips a percentage of values.

    The `pct` is a floating point value between 0.0 and 1.0. If the value is
    larger than 1.0 this will iterate every value. If this value is less than
    or equal to zero this will iterate no values.

    As long as the `pct` is greater than 0.0 the first value will always be
    iterated.

    # Examples

    >>> list(yter.percent(range(10), 0.25))
    [0, 4, 8]
    >>> list(yter.percent(range(10, -0.1)))
    []
    >>> list(yter.percent(range(10), 1.5))
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    """
    if pct <= 0.0:
        return
    if pct >= 1.0:
        for val in y:
            yield val
        return

    num, denom = float(pct).as_integer_ratio()
    count = denom
    for val in y:
        if count >= denom:
            yield val
            count += num
            count -= denom
        else:
            count += num


def flat(y):
    """Iterator of values from a iterable of iterators.

    This removes a level of nesting. When given a list of lists this will
    iterate the values from those children lists.

    This will invert the results of the `yter.chunk` iterator.

    # Examples

    >>> list(yter.flat([[1, 2], [3, 4, 5]]))
    [1, 2, 3, 4, 5]
    >>> list(yter.flat([range(3), range(6, 3, -1)]))
    [0, 1, 2, 6, 5, 4]

    # Implementation notes

    This is the same as `itertools.chain.from_iterable` with a more memorable
    name.
    
    """
    return itertools.chain.from_iterable(y)


def chunk(y, size):
    """Iterator of lists with a fixed size from iterable.

    Group the values from the iterable into lists up to a given size. The final
    list generated can be smaller than the given size.

    # Examples

    >>> tuple(yter.chunk(range(10), 3))
    ([0, 1, 2], [3, 4, 5], [6, 7, 8], [9])
    >>> tuple(yter.chunk([], 10))
    ()

    # Implementation notes

    The iterator will be advanced by the given ``size`` each time it
    is iterated.
    
    """
    if size <= 1:
        for val in y:
            yield [val]
    y = iter(y)
    _len = len
    while 1:
        values = list(itertools.islice(y, size))
        # Get size before yielding to avoid external tampering
        l = _len(values)
        if values:
            yield values
        if l < size:
            break


def key(y, key):
    """Iterator of pairs of key result and original values

    Each value will be a tuple with the return result of the `key` function and
    the actual value itself. The `key` function will be called with each value
    of the input iterator.

    This allows passing the generator to functions like `min` and `sorted`, but
    you are able to see the value and the result of the key argument.

    # Examples

    >>> list(yter.key(["one", "two", "three"], str.upper))
    [('ONE', 'one'), ('TWO', 'two'), ('THREE', 'three')]
    >>> list(yter.key(range(7), lambda x: x % 3))
    [(0, 0), (1, 1), (2, 2), (0, 3), (1, 4), (2, 5), (0, 6)]

    """
    # return ((key(val), val) for val in y)
    for val in y:
        result = key(val)
        yield (result, val)


def choose(y, key=None):
    """Separate iterators for true and false values.

    Creates two iterators that represent value that are false and values that
    are true. A key function can be given that will be used to provide the
    value's true or false state.

    # Examples

    >>> yes, no = yter.choose([0.0, 1.0, 2.0, 3.0])
    >>> list(yes)
    [1.0, 2.0, 3.0]
    >>> list(no)
    [0.0]

    # Implementation notes
    
    Internally this uses an `itertools.tee` to allow separate iterators
    over the same data. This will only call the key or nonzero boolean
    evaluation once per item.
    
    """
    key = key or bool
    y1, y2 = itertools.tee((key(v), v) for v in y)
    trues = (v for k, v in y1 if k)
    falses = (v for k, v in y2 if not k)
    return trues, falses


def unique(y, key=None):
    """Iterate only the unique values

    Only the first time a value is encountered it will be iterated. After that,
    values that are the same will be ignored.

    If the key is given, then it will be called on each value before comparing
    for uniqueness.

    # Examples

    >>> list(yter.unique([1, 2, 3, 2, 1]))
    [1, 2, 3]
    >>> list(yter.unique(["red", "RED", "Green"], str.lower))
    ['red', 'Green']

    # Implementation notes

    This uses a ``set`` to track which objects have already been found.
    
    """
    seen = set()
    seenadd = seen.add
    if key:
        for val in y:
            keyed = key(val)
            if keyed not in seen:
                seenadd(keyed)
                yield val
    else:
        for val in y:
            if val not in seen:
                seenadd(val)
                yield val


def duplicates(y, key=None):
    """Iterate only the duplicated values

    Will iterate a value for each time it is duplicated. If the iterator has
    three of the same value this will iterate the final two of them.

    If the key is given, then it will be called on each value before comparing
    for duplicates.

    # Examples

    >>> list(yter.duplicates([1, 2, 3, 2, 1]))
    [2, 1]
    >>> list(yter.duplicates(["red", "RED", "Green"], str.lower))
    ['RED']

    # Implementation notes

    This uses a ``set`` to track which objects have already been found.
    
    """
    seen = set()
    seenadd = seen.add
    if key:
        for val in y:
            keyed = key(val)
            if keyed not in seen:
                seenadd(keyed)
            else:
                yield val
    else:
        for val in y:
            if val not in seen:
                seenadd(val)
            else:
                yield val


def recurse(y, call):
    """Recurse values from a callable.
    
    Iterate a breadth first recursion using the given callable and an
    initial iterator of values. The callable is expected to return its
    own iterable of children or None, while taking an argument of a single
    item from the iterators.

    This will ensure only unique values are iterated, which avoids typical
    infinite recursion problems with recursive data structures.

    # Examples

    >>> friends = {
    ...    "alice": ["bob", "terry"], 
    ...    "bob": ["edward", "dave"],
    ...    "dave": ["alice", "bob"],
    ...    "edward": ["dave", "alice"],
    ...    "gary": ["dave", "bob"],
    ... }
    >>> list(yter.recurse(["alice"], friends.get))
    ['alice', 'bob', 'terry', 'edward', 'dave']

    # Implementation notes

    The callable results are treated as an iterator and will not be
    iterated until the caller reaches that data.

    This does not use function recursion, which avoids Python's typical
    stack limits encountered with deep data structures.
    
    """
    iters = [iter(y)] # Will iterate while modifying this list
    recursion = itertools.chain.from_iterable(iters)
    for item in unique(recursion):
        yield item
        kids = call(item)
        if kids:
            iters.append(kids)
