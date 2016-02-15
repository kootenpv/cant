"""Working on chaining results from remember. """

import copy

from cant.arity import PassAnything
from cant.rem import remember


class NoValidResultError(Exception):
    pass


def call_self_by_arity(fn, x, arity):
    if isinstance(fn, str):
        fn = getattr(x, fn)
    try:
        if arity == '1':
            return fn(x)
        else:
            return fn()
    except:
        raise NoValidResultError


def depth_two(inp, expected, args):
    results = []
    depth_2_template = '{}.{}({}) = {} ---> {}.{}({}) = {}'
    for x in remember(inp, PassAnything(), args):
        newinp = copy.copy(inp)
        try:
            res = call_self_by_arity(x['callable'], newinp, x['arity'])
            arg1 = args if x['arity'] == '1' else ''
        except NoValidResultError:
            continue
        try:
            n = remember(res, expected, args)
        # catching Python 2.x:
        # TypeError: object.__new__(listiterator) is not safe, use listiterator.__new__()
        except TypeError:
            continue
        oldinp = copy.copy(newinp)
        for r in n:
            if r['arity'] == '1':
                arg2 = args
            elif r['arity'] == 'starred':
                arg2 = '*' + str(args)
            else:
                arg2 = ''
            results.append(
                depth_2_template.format(
                    inp, x['callable'], arg1, res, res, r['callable'], arg2, expected
                )
            )
    return results
