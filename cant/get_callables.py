"""
Contains functions that provides ways to get important callables.
Such as builtins, globals, object callable attributes and module callable attributes.
"""

try:
    import __builtin__ as builtins
except ImportError:
    import builtins


def get_builtins(exclude_list=None):
    """ Gets the builtins functions and filters the functions that cause disturbance. """
    if exclude_list is None:
        exclude_list = ['input', '_dreload', 'dreload', 'open', 'help', 'license']
    return [getattr(builtins, x) for x in dir(builtins) if x not in exclude_list]


def protect_global_attrs(globals_dict):
    """
    Expects `globals()` fed to it.
    Removes troublemakers that cause disturbance.
    """
    attrs = [v for v in globals_dict.values()
             if hasattr(v, '__call__')
             and 'ipython' not in str(v).lower()
             and 'input' not in str(v).lower()
             and 'dreload' not in str(v).lower()
             and open != v
             and not str(v).startswith('<function test_')
             and not str(v).startswith('<function remember')]
    return attrs


def get_object_attrs(obj):
    """ Get the string names of all attributes of object `obj`.
    Implementation might change.
    """
    return dir(obj)


def get_module_attrs(obj):
    """ Get the potentially callable attributes of object `obj`. """
    return [getattr(obj, x) for x in dir(obj)]


def _type_dir(t):
    class T():

        def __call__(self, x):
            return getattr(x, t)

        def __repr__(self):
            return "getattr(__input__, '{}')".format(t)
    return T()


def get_type_dir():
    return [_type_dir(t) for t in dir(type)]
