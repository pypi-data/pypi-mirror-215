# yter

Version 3.0.0
2023, June 23

Clever, quick iterator functions that make your smile whiter.

This will work with versions of Python 2.6+ and 3.2+.


## Functions

There are many functions that process data from iterators in efficient ways.

* `yany` -- Extended version of the builtin any, test if any values are true
* `yall` -- Extended version of the builtin all, test if all values are true
* `ylen` -- Complete an iterator and get number of values
* `first` -- Get the first value from an iteraterable
* `last` -- Get the final value from an iteraterable
* `head` -- Get the first values from an iteraterable
* `tail` -- Get the last values from an iteraterable
* `minmax` -- Find the minimum and maximum values from an iterable
* `isiter` -- Test if an object is iterable, but not a string type
* `uniter` -- Efficient copy of non sequence data
* `repeat` -- Efficient lazy copy of non sequence data


## Iterators

There are several iterators that wrap an existing iterator and process it's output.

* `call` -- Iterator that works with mixed callable types
* `percent` -- Iterator that skips a percentage of values
* `flat` -- Iterator of values from a iterable of iterators
* `chunk` -- Iterator of lists with a fixed size from iterable
* `key` -- Iterator of pairs of key result and original values
* `choose` -- Split into iterators for true and false values
* `unique` -- Iterate only the unique values
* `duplicates` -- Iterate only the duplicated values


## Keys

Utility functions that are useful to use as a key argument

* `format` -- Create a function that formats given values into strings
* `numeric` -- Split a string into string and integer sections
* `getter` -- Shorthand for attrgetter, itemgetter, and methodcaller operators


[More documentation](https://gitlab.com/shredwheat/yter/blob/master/docs/docs/index.md) found in the repository.
