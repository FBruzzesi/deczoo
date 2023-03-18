<img src="docs/img/deczoo-logo.png" width=185 height=185 align="right">

![](https://img.shields.io/github/license/FBruzzesi/deczoo)
<img src ="docs/img/interrogate-shield.svg">
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Deczoo

> A zoo for decorators

There are many great decorators out there that we use everyday. Why don't collect few of them?

I found myself implementing over and over in different projects. The hope is to gather them here and use this codebase.

---

**Documentation**: https://fbruzzesi.github.io/deczoo

**Source Code**: https://github.com/fbruzzesi/deczoo

---

## Alpha Notice

This codebase is experimental and is working for my use cases. It is very probable that there are cases not covered and for which it breaks (badly). If you find them, please feel free to open an issue in the [issue page](https://github.com/FBruzzesi/deczoo/issues) of the repo.

## What is a decorator?

In short a python decorator is a way to modify or enhance the behavior of a function or a class without actually modifying the source code of the function or class.

Decorators are implemented as functions (or classes) that take a function or a class as input and return a new function or class that has some additional functionality.

To have a more in-depth explanation you can check the [decorators docs page](https://fbruzzesi.github.io/deczoo/decorators/intro/).

## Installation

**deczoo** is published as a Python package on [pypi](https://pypi.org/), and it can be installed with pip, or directly from source using git, or with a local clone:

### pip

```bash
python -m pip install deczoo
```

### source/git

```bash
python -m pip install git+https://github.com/FBruzzesi/deczoo.git
```

### local clone

```bash
git clone https://github.com/FBruzzesi/deczoo.git
cd deczoo
python -m pip install .
```

### Dependencies

As of now, the library has no additional required dependencies, however:

- some functionalities works only on UNIX systems (`@memory_limit` and `@timeout`)
- to use some decorators you may need to install additional dependencies (e.g. install [`chime`](https://github.com/MaxHalford/chime) to use `@chime_on_end`)

## Getting started

The idea is kind of simple: each function in the library is a (function) decorator with a specific objective in mind.

```python title="Example: log decorator"
from deczoo import log

@log # equivalent to @log(log_time=True, log_args=True, log_error=True, logging_fn=print)
def custom_add(a, b, *args):
    """Adds all arguments together"""
    return sum([a, b, *args])

_ = custom_add(1, 2, 3, 4)
# custom_add args=(a=1, b=2, args=(3, 4)) time=0:00:00.000062

 _ = custom_add(1, "a", 2)
# custom_add args=(a=1, b=a, args=(2,)) time=0:00:00.000064 Failed with error: unsupported
# operand type(s) for +: 'int' and 'str'
```

```python title="Example: shape_tracker decorator"
from deczoo import shape_tracker

@shape_tracker(shape_in=True, shape_out=True, shape_delta=True, raise_if_empty=True)
def tracked_vstack(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.vstack([a, b])

_ = tracked_vstack(np.ones((1, 2)), np.ones((10, 2)))
# Input: `a` has shape (1, 2)
# Output: result has shape (11, 2)
# Shape delta: (-10, 0)
```

### Features

The library implements the following decorators:

- `call_counter`: tracks how many times a function has been called.
- `catch`: wraps a function in a try-except block, returning a custom value, or raising a custom exception.
- `check_args`: checks that function arguments satisfy its "rule".
- `chime_on_end`: notify with chime sound on function end (success or error).
- `log`: tracks function time taken, arguments and errors, such logs can be written to a file.
- `timer`: tracks function time taken.
- `memory_limit`: sets a memory limit while running the function.
- `notify_on_end`: notifies when function finished running with a custom notifier.
- `retry`: wraps a function with a "retry" block.
- `shape_tracker`: tracks the shape of a dataframe/array-like object, in input and/or output.
- `multi_shape_tracker`: tracks the shapes of input(s) and/or output(s) of a function.
- `timeout`: sets a time limit for the function, terminates the process if it hasn't finished within such time limit.

### Examples

Please refer to the [api page](https://fbruzzesi.github.io/deczoo/api/decorators/) to see a basic example for each decorator.

## Contributing

Please read the [Contributing guidelines](https://fbruzzesi.github.io/deczoo/contribute/) in the documentation site.

## License

The project has a [MIT Licence](https://github.com/FBruzzesi/deczoo/blob/main/LICENSE)
