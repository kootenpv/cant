""" Main functionality module. Contains the "remember" main function. """

import copy
import os
import sys

from cant.arity import arity_one, arity_one_self, arity_one_starred, \
    arity_starred, arity_two, arity_zero
from cant.comparison_functions import safe_equal
from cant.get_callables import get_builtins, get_module_attrs, get_object_attrs, \
    protect_global_attrs


def loop_over(container, name, inp, expected, eq_fn, args, options):
    """ Loops over the functions in container and tries all arities on it
        to give results that contain that pass the equality_function test. """
    sys.stdout = open(os.devnull, "w")
    for callab in container:
        options.extend([arity_zero(callab, inp, expected, eq_fn, name),
                        arity_one_self(callab, inp, expected, eq_fn, name)])
        if args is not None:
            options.extend([arity_one(callab, inp, expected, eq_fn, name, args),
                            arity_starred(callab, inp, expected, eq_fn, name, args),
                            arity_one_starred(callab, inp, expected, eq_fn, name, args),
                            arity_two(callab, inp, expected, eq_fn, name, args)])
    sys.stdout = sys.__stdout__


def remember(inp, expected, args=None, equality_function=safe_equal,
             globals_dict=None,
             builtins_namespace=False,
             custom_namespace=None,
             module_namespace=None):
    """ Main function. Go read the GitHub README for the story. """
    options = []
    # also add option to switch x and args (mirror)
    sys.stdout = open(os.devnull, "w")

    loop_over(get_object_attrs(copy.copy(inp)), 'self', inp,
              expected, equality_function, args, options)

    if globals_dict is not None:
        global_functions = protect_global_attrs(globals_dict)
        loop_over(global_functions, 'global', inp, expected, equality_function, args, options)

    if builtins_namespace:
        loop_over(get_builtins(), 'builtins', inp, expected, equality_function, args, options)

    if custom_namespace is not None:
        loop_over(custom_namespace, 'custom', inp, expected, equality_function, args, options)

    if module_namespace is not None:
        loop_over(get_module_attrs(module_namespace), module_namespace.__name__,
                  inp, expected, equality_function, args, options)

    sys.stdout = sys.__stdout__
    return [y for y in options if y]
