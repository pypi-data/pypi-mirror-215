"""Import everything from itertools, more_itertools and some custom functions """
from __future__ import annotations

import warnings
from math import inf
from typing import Iterable, Any, Type, Tuple, Iterator, Protocol, TypeVar, TYPE_CHECKING

from itertools import *
from more_itertools import *

if TYPE_CHECKING:
    from _typeshed import SupportsAdd, SupportsSub, SupportsAllComparisons


    class SupportsAddSub(SupportsAdd[Any], SupportsSub[Any], Protocol):
        ...


    class SupportsAddSubComparison(SupportsAddSub[Any], SupportsAllComparisons[Any], Protocol):
        ...


    SupportsAddSubT = TypeVar('SupportsAddSubT', bound=SupportsAddSub)
    SupportsAddSubComparisonT = TypeVar('SupportsAddSubComparisonT',
                                        bound=SupportsAddSubComparison)


def separate_iterator(it: Iterable, sep: Any) -> Iterator:
    """separate_iterator('abcde', ',') --> a , b , c , d , e

    The same as :func:`~more_itertools.intersperse(sep, it, n=1)`. Only here for backwards compability.
    """
    warnings.warn(f"{__name__}.separate_iterator is just a wrapper around intersperse.",
                  DeprecationWarning,
                  stacklevel=2)
    return intersperse(sep, it, n=1)


def flatten_nested(it: Iterable, dtypes: Tuple[Type[Iterable], ...] = (list,)) -> Iterator:
    """Flattens the given arbitrarily nested iterable. By default, only lists are flattened. Use the optional `dtypes`
    argument to flatten other iterables as well.

    Similar to :func:`~more_itertools.collapse` which works with a blacklist instead of a whitelist.

    Parameters
    ----------
    it: :class:`~typing.Iterable` to flatten
    dtypes: Types that get flattened.

    Returns
    -------
    Objects that are not of a type in `dtypes`
    """
    if isinstance(it, dtypes):
        for x in it:
            yield from flatten_nested(x, dtypes)
    else:
        yield it


def argmin(it: Iterable) -> int:
    """Return index of smallest element by iteration order.

    >>> argmin([1, 3, 2, 4, 0])
    4

    Raises
    --------
    :class:`~ValueError` if the iterable is empty.

    Parameters
    ----------
    it: :class:`~typing.Iterable` to search for minimum

    Returns
    -------
    Index of the smallest element if it by iteration order
    """
    it = enumerate(it)
    try:
        min_idx, current = next(it)
    except StopIteration:
        raise ValueError('Argument was empty')
    for idx, elem in it:
        if elem < current:
            current = elem
            min_idx = idx
    return min_idx


def argmax(it: Iterable) -> int:
    """Return index of largest element by iteration order.

    >>> argmax([1, 3, 2, 4, 0])
    3

    Raises
    --------
    :class:`~ValueError` if the iterable is empty.

    Parameters
    ----------
    it: :class:`~typing.Iterable` to search for maximum

    Returns
    -------
    Index of the largest element if it by iteration order
    """
    it = enumerate(it)
    try:
        max_idx, current = next(it)
    except StopIteration:
        raise ValueError('Argument was empty')
    for idx, elem in it:
        if elem > current:
            current = elem
            max_idx = idx
    return max_idx


def next_largest(it: Iterable[SupportsAddSubComparisonT],
                 value: SupportsAddSubT) -> SupportsAddSubT:
    """Return the next-largest element to value from it.

    Parameters
    ----------
    it: Iterable
        The iterable to search.
    value: number-like
        The number to find the next-largest element to.

    Returns
    -------
    The next-largest element to value in it, or the value itself if it
    is empty.

    Examples
    --------
    >>> next_largest([3, 4, 1, -5], 2.7)
    3.0
    >>> next_largest([3, 4, 1, -5], 1.01)
    3.0
    >>> next_largest([3, 4, 1, -5], -10)
    -5
    >>> next_largest([3, 4, 1, -5], 7.123)
    4
    >>> next_largest([1, 2, 10321], inf)
    10321
    >>> next_largest([], 42)
    42

    Notes
    -----
    If you don't mind loading the elements into memory, the following
    will almost certainly be faster (not accounting for corner cases)::

        import bisect
        def next_largest(it, value):
            sorted_it = sorted(it)
            idx = bisect.bisect_right(sorted_it, value)
            return sorted_it[idx]

    """
    if value == inf:
        return max(it, default=inf)
    if value == -inf:
        return min(it, default=-inf)

    smallest_distance = inf
    largest = -inf
    for x in it:
        if 0 <= (distance := x - value) < smallest_distance:
            smallest_distance = distance
        # Need to keep track of smallest value in case val is outside the interval of it
        if largest < x <= value:
            largest = x

    if largest == -inf:
        # empty iterable or +inf
        largest = value
    if smallest_distance == inf:
        # no item in it larger than value
        return largest
    return smallest_distance + value


def next_smallest(it: Iterable[SupportsAddSubComparisonT],
                  value: SupportsAddSubT) -> SupportsAddSubT:
    """Return the next-smallest element to value from it.

    Parameters
    ----------
    it: Iterable
        The iterable to search.
    value: number-like
        The number to find the next-largest element to.

    Returns
    -------
    The next-largest element to value in it, or the value itself if it
    is empty.

    Examples
    --------
    >>> next_smallest([3, 4, 1, -5], 2.7)
    1.0
    >>> next_smallest([3, 4, 1, -5], 1.01)
    1.0
    >>> next_smallest([3, 4, 1, -5], -10)
    -5
    >>> next_smallest([3, 4, 1, -5], 7.123)
    4.0
    >>> next_smallest([1, 2, 10321], inf)
    10321
    >>> next_smallest([], 42)
    42

    Notes
    -----
    If you don't mind loading the elements into memory, the following
    will almost certainly be faster (not accounting for corner cases)::

        import bisect
        def next_smallest(it, value):
            sorted_it = sorted(it)
            idx = bisect.bisect_left(sorted_it, value)
            return sorted_it[idx]

    """
    if value == inf:
        return max(it, default=inf)
    if value == -inf:
        return min(it, default=-inf)

    # This could be a lot simpler if corner cases need not be respected, such as if value is
    # outside the interval of it.
    largest_distance = -inf
    smallest = inf
    for x in it:
        if 0 >= (dist := x - value) > largest_distance:
            largest_distance = dist
        # Need to keep track of smallest value in case value is outside the interval of it
        if smallest > x >= value:
            smallest = x

    if smallest == inf:
        # empty iterable or -inf
        smallest = value
    if largest_distance == -inf:
        # no item in it larger than value
        return smallest
    return largest_distance + value


def next_closest(it: Iterable[SupportsAddSubComparisonT],
                 value: SupportsAddSubT) -> SupportsAddSubT:
    """Return the next-closest element to value from it.

    Parameters
    ----------
    it: Iterable
        The iterable to search.
    value: number-like
        The number to find the next-largest element to.

    Returns
    -------
    The next-closest element to value in it, or the value itself if it
    is empty.

    Examples
    --------
    >>> next_closest([3, 4, 1, -5], 2.7)
    3
    >>> next_closest([3, 4, 1, -5], 1.01)
    1
    >>> next_closest([3, 4, 1, -5], -10)
    -5
    >>> next_closest([3, 4, 1, -5], 7.123)
    4
    >>> next_closest([1, 2, 10321], inf)
    10321
    >>> next_closest([], 42)
    42

    """
    if value == -inf:
        return min(it, default=value)
    elif value == inf:
        return max(it, default=value)
    return min(it, key=lambda x: abs(x - value), default=value)


def ignore_exceptions(it: Iterable, exceptions: Any) -> Iterator:
    """Ignore all specified exceptions during iteration.

    >>> list(ignore_exceptions(map(lambda d: 5 / d, [2, 1, 0, 5]), ZeroDivisionError))
    [2.5, 5.0, 1.0]

    Be aware that some iterators do not allow further iteration if they threw an exception.
    >>> list(ignore_exceptions((5 / d for d in [2, 1, 0, 5]), ZeroDivisionError))
    [2.5, 5.0]

    Parameters
    ----------
    it: :class:`~typing.Iterable` to iterate over.
    exceptions: Valid argument to an ``except`` clause
    """
    it = iter(it)
    while True:
        try:
            yield from it
        except exceptions:
            continue
        else:
            return


del Iterable, Any, Type, Tuple, Iterator
del warnings
