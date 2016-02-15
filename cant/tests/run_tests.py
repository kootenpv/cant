""" Contains py.test tests. """

import sys
sys.path.append('../..')

from cant.alpha_status import depth_two
from cant.arity import PassAnything
from cant.rem import remember


# TODO: Maybe make strings more specific (discover how they come back)
# TODO: Merge having multiple cases and only keep results present in both

# Test wrapper


def result_contains_callable(test_result, call):
    """ Wrapper for confirming the method call is found in the test result. """
    return any([call in str(x['callable']) for x in test_result])


# Class instance methods testing (@classmethod is included)

class TestClassInstanceMethods(object):
    """ Class that contains an instance method and a class method """
    meaning_of_line = 42

    def some_instance_method(self):
        """ Returns the meaning of life. """
        return self.meaning_of_line

    @classmethod
    def class_method(cls):
        """ Returns the meaning of life. """
        return 42


def test_class_instance_methods():
    """
    Testing whether a class' instance method can be used.
    Testing whether a class' class method can be used.
    """
    inp = TestClassInstanceMethods()
    expected = 42
    assert result_contains_callable(remember(inp, expected), 'some_instance_method')
    assert result_contains_callable(remember(inp, expected), 'class_method')


# General

def test_pass_anything():
    """ Testing whether PassAnything class works when expecting no value, just no errors. """
    inp = 42
    expected = PassAnything()
    assert result_contains_callable(remember(inp, expected), '__add__')


def test_general_set_union():
    """ Testing whether set union is found for combining sets. """
    inp = set([2, 3])
    args = [3, 4]
    expected = set([2, 3, 4])
    assert result_contains_callable(remember(inp, expected, args), 'union')


def test_general_set_intersection():
    """ Testing whether set difference is not found for not overlapping sets. """
    inp = set([2, 3])
    args = [4]
    expected = set()
    assert result_contains_callable(remember(inp, expected, args), 'intersection')


def test_general_set_intersection2():
    """ Testing whether set intersection is found for overlapping sets. """
    inp = set([2, 3])
    args = [3, 5]
    expected = set([3])
    assert result_contains_callable(remember(inp, expected, args), 'intersection')


def test_general_set_pop_arity1():
    """ Testing set.pop (which takes no arguments) and return 2. """
    inp = set([2, 3, 4])
    expected = 2
    assert result_contains_callable(remember(inp, expected), 'pop')


def test_general_set_difference():
    """ Testing whether set difference is found for overlapping sets. """
    inp = set([5, 6, 7, 8])
    args = set([5, 8])
    expected = set([6, 7])
    assert result_contains_callable(remember(inp, expected, args), 'difference')


def test_general_integer_add():
    """ Testing whether integer add is found to solve 42+42=84. """
    inp = 42
    args = 42
    expected = 84
    assert result_contains_callable(remember(inp, expected, args), 'add')

# Module test


def test_module_itertools():
    """ Testing the module scope. """
    import itertools
    inp = [1, 2, 3]
    args = 2
    expected = [(1, 2), (1, 3), (2, 3)]
    assert result_contains_callable(remember(inp, expected, args, module_namespace=itertools),
                                    'itertools.combinations')

# Globals

TEST_CURRENT_GLOBALS = globals()


def global_arity_0():
    """ Function loaded in the current scope for an arity of 0 example """
    return 42


def test_global_arity0():
    """ Test whether the above current scope function can be used to solve this case """
    inp = 1
    expected = 42
    assert result_contains_callable(remember(inp, expected, globals_dict=TEST_CURRENT_GLOBALS),
                                    'global_arity_0')


def global_arity_1(inp):
    """ Function loaded in the current scope for an arity of 1 example """
    if inp == 1:
        return 42
    else:
        return -42


def test_global_arity1():
    """ Test whether the above current scope function can be used to solve this case """
    inp = 1
    expected = 42
    assert result_contains_callable(
        remember(inp, expected, globals_dict=globals()), 'global_arity_1')

# for test_math_ceil
from math import *


def test_math_ceil():
    """ Test whether the above current scope function can be used to solve this case """
    inp = 12.1
    expected = 13
    assert result_contains_callable(
        remember(inp, expected, globals_dict=globals()), 'ceil')


# Builtins


def test_builtins_float():
    """ Testing whether builtins can be used to solve. """
    inp = 10
    expected = 10.0
    assert result_contains_callable(remember(inp, expected, builtins_namespace=True), 'float')


def test_builtins_str():
    """ Testing whether builtins can be used to solve. """
    inp = 1
    expected = '1'
    assert result_contains_callable(remember(inp, expected, builtins_namespace=True), 'str')


# Depth two

def test_depth_two():
    inp = [5]
    expected = 15
    args = 3
    depth_two(inp, expected, args)
