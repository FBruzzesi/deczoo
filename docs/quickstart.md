
# Getting started

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

## Features

The library implements the following decorators:

- `call_counter`: Counts how many times a function has been called
- `catch`: Wraps a function in a try-except block
- `check_args`: Checks that function arguments satisfy given rules
- `chime_on_end`: Notify with chime sound on function end
- `log`: Tracks function time taken, arguments and errors
- `timer`: Tracks function time taken
- `memory_limit`: Sets a memory limit for a function
- `notify_on_end`: notifies you when a function finished with a custom notifier
- `retry`: Wraps a function with a retry block
- `timeout`: Sets a time limit to a function to run

## Examples

Please refer to the [api page](https://fbruzzesi.github.io/deczoo/api/decorators/) to see a basic example for each decorator.
