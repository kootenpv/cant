""" Rather than doing a simple `==` comparison, this module contains functions
that could be better suited to do comparisons. """

try:
    from itertools import izip_longest as zip_longest
except ImportError:
    # pylint: disable=no-name-in-module
    from itertools import zip_longest


def safe_equal(var1, var2):
    """ safe_equal could also work for generators. """
    if hasattr(var1, '__iter__') and hasattr(var2, '__iter__'):
        return all(x == y for x, y in zip_longest(var1, var2))
    return var1 == var2
