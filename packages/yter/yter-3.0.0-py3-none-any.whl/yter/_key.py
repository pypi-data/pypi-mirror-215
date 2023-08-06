"""Functions that make useful keys"""

import re
import operator


def format(fmt, **kwargs):
    """Create a function that formats given values into strings.

    Additional keywoard arguments can be given that will also be passed to the
    format function.

    The value passed to the function will be given as the first argument to
    format, which is referenced as {0}.

    # Examples

    >>> pct = yter.format("{:!<5.0%} odds")
    >>> list(pct(v) for v in (.25, .5, 1))
    ['25%!! odds', '50%!! odds', '100%! odds']
    >>> renamer = yter.format("{0.stem}.{ext}, ext="py")
    >>> {p: renamer(p) for p in paths}

    """
    def formatted(val):
        return fmt.format(val, **kwargs)
    return formatted


NUMBER_REGEX = None


def numeric(value):
    """Split a string into string and integer sections.

    A string will be a tuple containing sections that are strings and integers.
    The numeric parts of the string will be converted into integers.
    The first value in the result will always be a string. If the value argument
    starts with numbers then this will be an empty string. This ensures results
    from any ``numeric`` call can be compared with others.

    Negative numbers will also be converted if preceded by a single minus sign.
    This does not attempt to handle floating point numbers, instead those
    will be split into two integers with a single character string in the middle.

    # Examples

    >>> yter.numeric("one01two2")
    ['one', 1, 'two', 2, '']
    >>> yter.numeric("1one-2two")
    ['', 1, 'one', -2, 'two']
    >>> yter.numeric("one01two2") < yter.numeric("1one-2two")
    False
    >>> yter.numeric("pi starts with 3.14")
    ['pi starts with ', 3, '.', 14]

    """
    global NUMBER_REGEX

    if not value:
        return ()

    if not NUMBER_REGEX:
        NUMBER_REGEX = re.compile(r"(-?\d+)")
    parts = iter(NUMBER_REGEX.split(value))

    # Values that start with digits will get a leading empty string
    converted = []
    try:
        while True:
            val1 = next(parts)
            converted.append(val1)
            val2 = next(parts)
            converted.append(int(val2))
    except StopIteration:
        pass
    # When value ends with a digit drop the trailing empty string
    if converted[-1] == "":
        converted.pop()
    return tuple(converted)


class _GetterImpl(object):
    """Shorthand for the attrgetter, itemgetter, and methodcaller operators.

    The same results can be achieved by using `operator.attrgetter` and
    `operator.itemgetter`, but this is more concise and can also be used to
    lookup nested data.

    By using the special syntax, `getter._(args)` you can also create a
    callable. This is similar to the `operator.methodcaller` but it doesn't use
    a method name. The underscore attribute can be called to create a callable
    lookup, which can still be chained with item and attributes.

    If an attribute or item is not found this will result in None instead of an
    exception, which is more useful for key functions.

    You can lookup multiple items by passing multiple values to the index
    operator.

    Looking up attributes can only be done with a single value.

    # Examples

    >>> data = {"name": {"first": "Peter", "last": "Shinners"}, "id": 1234}
    >>> key = yter.getter["name"]["first"]
    >>> print(key(data))
    "Peter"
    >>> print(yter.getter.real(1.2))
    1.2
    >>> data = [bool, int, float, str]
    >>> print [yter.getter._("12") for d in data]
    [True, 12, 12.0, '12']

    # Implementation details

    This combines the `operator.attrgetter` and `operator.itemgetter` as well
    as its own logic for handling callable objects.
    
    """

    def __init__(self, getters):
        self.__getters = getters

    def __getitem__(self, vals):
        if isinstance(vals, tuple):
            get = operator.itemgetter(*vals)
        else:
            get = operator.itemgetter(vals)
        key = type(self)(self.__getters + (get,))
        return key

    def __getattr__(self, name):
        get = operator.attrgetter(name)
        key = type(self)(self.__getters + (get,))
        return key

    @property
    def _(self):
        def _makecaller(*args, **kwargs):
            def get(val):
                return val(*args, **kwargs)
            key = type(self)(self.__getters + (get,))
            return key
        return _makecaller

    def __call__(self, value):
        try:
            for get in self.__getters:
                value = get(value)
        except KeyError:
            return None
        except AttributeError:
            return None
        return value


getter = _GetterImpl(())
