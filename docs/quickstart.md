# Getting started

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

## Features

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

## Examples

Please refer to the [api page](api/decorators.md) to see a basic example for each decorator.
