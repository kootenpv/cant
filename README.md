## cant

The main idea was that sometimes I know it is possible to get some output given some input but I forgot the name of the function I'm looking for. This module can find that function for you. Some kind of reverse engineering if you will.

Specify the `input` and `expected` value. Optionally you can give it arguments.

It then uses:

- `globals`
- functions from a module
- `builtins`
- the object's methods, and
- class methods

in an attempt to find functions that that can bring `inp` to `expected`.

E.g.:

    # The following will give '__mul__' as an option
    remember(inp=5, expected=15, args=3)

    # since
    5.__mul__(3) == 15

Obviously you don't need help with this particular case. But it gets interesting when you throw in your own classes into the mix, or you just know e.g. the module, but not the function that can get the required output; has happened to me with `itertools` (hint: look in [run_tests.py](https://github.com/kootenpv/cant/blob/master/cant/tests/run_tests.py) examples).

This was a great practice for working with all kinds of arities (0, 1, starred, 1+starred, 2) and scopes (global, modules, objects, builtins).

**Warning**: it makes copies of all simple objects to enable using functions that modify the object in place and while not affecting the "outside" scope. However, database stuff etc that would not be able to be rolled back by `copy` should be considered unsafe.

### Usage

Use the `cant.remember` function to find all functions that bring `inp` (and optionally, `args`) to `expected`, e.g.:

```python
[In]  cant.remember(inp=5, expected=15, args=3)

[Out] [{'arity': '1', 'callable': '__mul__', 'input': 5, 'namespace': 'self'},
       {'arity': '1', 'callable': '__rmul__', 'input': 5, 'namespace': 'self'}]
```

Use the `cant.depth_two` (alpha-status; should be generalized to `depth_n`) function to find all functions that go depth two, e.g.:

```python
[In]  cant.depth_two(inp=[5], expected=15, args=3)

[Out] ['[5].pop() = 5 ---> 5.__mul__(3) = 15',
       '[5].pop() = 5 ---> 5.__rmul__(3) = 15']
```
What happens there is that it considers all possibilities, and the first that works is:

- use the attribute `pop` of the list input object `[5]`
- take the value of `[5].pop()` which is `5`
- out of all the options for the object `5`, use `__mul__`
- `inp.pop().__mul__(args) == expected` was found to hold (`5*3==15`)

Actually, in the example above it tried all possible combinations at both levels and found `pop`ping and using `__mul__` to be satisfying the `input -> ... -> expected` condition.

See `tests/run_tests.py` for more/documented examples.

### Installation

`tox` tests for Python 2.7, Python 3.4 and Python 3.5: all tests pass.

It's on pip:

    pip install cant
