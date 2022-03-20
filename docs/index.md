<img src="img/icon.png" width=185 height=185 align="right">

# deczoo
> A zoo for decorators

There are many great decorators out there that we use everyday.

However there are also few decorators that I found myself implementing over and over in different projects. The hope is to gather them here and use this codebase.

## Alpha Notice
This package is really new and there are edge cases that probably doesn't cover (yet).

## Installation

You can install the library using `pip`:

```bash
python -m pip install deczoo
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


## Feedbacks and Contributing

Any feedback, improvement/enhancement or issue is welcome in the [issue list](https://github.com/FBruzzesi/deczoo/issues) of the repo.

To get started locally, you can clone the repo and quickly get started using the `Makefile`.

```
git clone git@github.com:FBruzzesi/deczoo.git
cd deczoo
make init-develop
```
