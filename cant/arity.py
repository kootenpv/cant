""" This module contains the versions that test whether func(inp) == expected.
    In order to use a function, it has to be checked for multiple number of arguments.
    Either zero, one, one + starred, or two. """


# ADD ALSO ATTRIBUTE TESTS, e.g. yag.owner.login == 'kootenpv' when i was looking for owner

# TODO: I'm starting to think that I'm still missing a case with star args:
# - fn(*args), args
# - fn(*args), *args
# - fn(args), args
# - fn(args), *args
import copy


# I'm literally trying to catch ANY exception in arity.py.
# pylint: disable=bare-except


class PassAnything(object):
    """ When a PassAnything object is given to be evaluated, it will pass if there is no error. """
    # pylint: disable=too-few-public-methods
    pass


def get_copied_input_and_callable(inp, callab):
    """ collab remains either str or callable, while clb is callable
        in case of 'str', it's a sign also of "self" and it has to be getattr'ed
        I do this because class instance methods are now possible as well """
    safe_inp = copy.copy(inp)
    clb = getattr(safe_inp, callab) if isinstance(callab, str) else callab
    return safe_inp, clb


def arity_zero(callab, inp, expected, equality_fun, namespace):
    """ Only going to pass for functions that take NO arguments. """
    res = {}
    try:
        _, clb = get_copied_input_and_callable(inp, callab)
        if equality_fun(clb(), expected) or isinstance(expected, PassAnything):
            res = {'arity': '0', 'namespace': namespace, 'callable': callab}
    except:
        pass
    return res


def arity_one_self(callab, inp, expected, equality_fun, namespace):
    """ Only going to pass for functions that take 1 single argument. """
    res = {}
    try:
        safe_inp, clb = get_copied_input_and_callable(inp, callab)
        if equality_fun(clb(safe_inp), expected) or isinstance(expected, PassAnything):
            res = {'arity': '1', 'namespace': namespace, 'callable': callab,
                   'input': inp}
    except:
        pass
    return res


def arity_one(callab, inp, expected, equality_fun, namespace, args):
    """ Only going to pass for functions that take 1 single argument. """
    res = {}
    try:
        safe_inp, clb = get_copied_input_and_callable(inp, callab)
        print('FFFFFFFFFFFFFFFFWasdf')
        if equality_fun(clb(args), expected) or isinstance(expected, PassAnything):
            res = {'arity': '1', 'namespace': namespace, 'callable': callab,
                   'input': inp}
    except:
        pass
    return res


def arity_starred(callab, inp, expected, equality_fun, namespace, args):
    """ Only going to pass for functions that take only args, and will unpack them.
        The 'inp' variable is ignored for that function. """
    res = {}
    try:
        _, clb = get_copied_input_and_callable(inp, callab)
        # This is not an error; callable might not have an `x`
        # pylint: disable=no-value-for-parameter
        if equality_fun(clb(*args), expected) or isinstance(expected, PassAnything):
            res = {'arity': 'starred', 'namespace': namespace, 'callable': callab}
    except:
        pass
    return res


def arity_one_starred(callab, inp, expected, equality_fun, namespace, args):
    """ Only going to pass for functions that take 1 single argument and also starred args. """
    res = {}
    try:
        safe_inp, clb = get_copied_input_and_callable(inp, callab)
        if equality_fun(clb(safe_inp, *args), expected) or isinstance(expected, PassAnything):
            res = {'arity': '1+starred', 'namespace': namespace, 'callable': callab}
    except:
        pass
    return res


def arity_two(callab, inp, expected, equality_fun, namespace, args):
    """ Only going to pass for functions that take 2 arguments. """
    res = {}
    try:
        safe_inp, clb = get_copied_input_and_callable(inp, callab)
        if (equality_fun(clb(safe_inp, copy.copy(args)), expected)
                or isinstance(expected, PassAnything)):
            res = {'arity': '2', 'namespace': namespace, 'callable': callab}
    except:
        pass
    return res
