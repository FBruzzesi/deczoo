<img src="docs/img/icon.png" width=185 height=185 align="right">

# deczoo

> A zoo for decorators

There are many great decorators out there that we use everyday. Why don't collect few of them?

I found myself implementing over and over in different projects. The hope is to gather them here and use this codebase.

## Alpha Notice

This package is really new and there are edge cases that probably doesn't cover (yet).

## Installation

You can install the library using `pip`:

```bash
python -m pip install deczoo
```

## Getting started

We have a [documentation page](https://fbruzzesi.github.io/deczoo/) that explains how each feature works.

Each function here is a decorator with a specific objective in mind.

```python
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

## Features

The library implements few (function) decorators:

- `call_counter`: Counts how many times a function has been called
- `catch`: Wraps a function in a try-except block
- `check_args`: Checks that function arguments satisfy given rules
- `chime_on_end`: Notify with chime sound on function end
- `dump_result`: Saves function result in a pickle file
- `log`: Tracks function time taken, arguments and errors
- `timer`: Tracks function time taken
- `memory_limit`: Sets a memory limit for a function
- `retry`: Wraps a function with a retry block
- `timeout`: Sets a time limit to a function to run

## Feedbacks

Any feedback, improvement/enhancement or issue is welcome in the [issue page](https://github.com/FBruzzesi/deczoo/issues) of the repo.

## Contributing

Make sure to check the [issue list](https://github.com/FBruzzesi/deczoo/issues) beforehand.

 To get started locally, you can clone the repo and quickly get started using the `Makefile`:

```bash
git clone git@github.com:FBruzzesi/deczoo.git
cd deczoo
make init-develop
```

## Licence

This repository has a MIT Licence
