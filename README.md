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

## Installation

**deczoo** is published as a Python package on [pypi](https://pypi.org/), and it can be installed with pip, ideally by using a virtual environment (suggested option), or directly from source using git, or with a local clone:

- **pip**: `python -m pip install deczoo`
- **source/git**: `python -m pip install git+https://github.com/FBruzzesi/deczoo.git`
- **local clone**:
    ```bash
    git clone https://github.com/FBruzzesi/deczoo.git
    cd deczoo
    python -m pip install .
    ```

## Getting started

The idea is kind of simple: each function in the library is a (function) decorator with a specific objective in mind.

```python title="Example: log decorator"
from deczoo import log

@log # equivalent to @log(log_time=True, log_args=True, log_error=True, logging_fn=print)
def my_add_function(a, b, *args):
    """Adds all arguments together"""
    return sum([a, b, *args])

_ = my_add_function(1, 2, 3, 4)
# my_add_function args=(a=1, b=2, args=(3, 4)) time=0:00:00.000062

 _ = my_add_function(1, "a", 2)
# my_add_function args=(a=1, b=a, args=(2,)) time=0:00:00.000064 Failed with error: unsupported
# operand type(s) for +: 'int' and 'str'
```

### Features

The library implements the following decorators:

- `call_counter`: Counts how many times a function has been called
- `catch`: Wraps a function in a try-except block
- `check_args`: Checks that function arguments satisfy given rules
- `chime_on_end`: Notify with chime sound on function end
- `dump_result`: Saves function result in a pickle file
- `log`: Tracks function time taken, arguments and errors
- `timer`: Tracks function time taken
- `memory_limit`: Sets a memory limit for a function
- `notify_on_end`: notifies you when a function finished with a custom notifier
- `retry`: Wraps a function with a retry block
- `timeout`: Sets a time limit to a function to run

### Examples

Please refer to the [api page](https://fbruzzesi.github.io/deczoo/api/decorators/) to see a basic example for each decorator.

## Contributing

Please read the [Contributing guidelines](https://fbruzzesi.github.io/deczoo/contribute/) in the documentation site.

## License

The project has a [MIT Licence](https://github.com/FBruzzesi/deczoo/blob/main/LICENSE)
