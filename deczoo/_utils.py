from functools import partial, wraps
from typing import Callable, Protocol, Tuple, runtime_checkable

LOGGING_FN: Callable[[str], None]

try:
    from rich.console import Console
    from rich.theme import Theme

    custom_theme = Theme({"good": "bold green", "bad": "bold red"})
    console = Console(theme=custom_theme)

    LOGGING_FN = console.log

except ImportError:

    LOGGING_FN = print


def check_parens(decorator: Callable) -> Callable:
    """
    Check whether or not a decorator function gets called with parens:

    - If called with parens, the decorator is called without the function as the first
        argument, but necessarely with decorator keyword arguments.
    - If called without parens, the decorator is called with the function as the first
        argument, and the decorator's default arguments.

    This function is used internally to endow every decorator of the above property.

    Arguments:
        decorator: decorator to wrap

    Returns:
        Wrapped decorator.

    Usage:
    ```python
    @check_parens
    def decorator(func, k1="default1", k2="default2"):
        # where the magic happens
        ...

    # `decorator` called without parens, hence default params.
    @decorator
    def func(*func_args, **func_kwargs):
        pass

    # `decorator` called with custom params, necessarely using parens.
    @decorator(*args, **kwargs)
    def func(*func_args, **func_kwargs):
        pass
    ```
    """

    @wraps(decorator)
    def wrapper(func: Callable = None, *args, **kwargs) -> Callable:

        if func is None:
            return partial(decorator, *args, **kwargs)
        else:
            return decorator(func, *args, **kwargs)

    return wrapper


def _get_free_memory() -> int:
    """
    Computes machine free memory via `/proc/meminfo` file (linux only).

    **Warning**: This functionality is supported on unix-based systems only!
    """

    with open("/proc/meminfo", "r") as mem:
        free_memory = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) in ("MemFree:", "Buffers:", "Cached:"):
                free_memory += int(sline[1])
    return free_memory


@runtime_checkable
class HasShape(Protocol):
    """
    Protocol for objects that have a shape attribute.
    In this context, a "dataframe"-like object.
    """

    @property
    def shape(self) -> Tuple[int, ...]:
        pass


class EmptyShapeError(Exception):
    """Exception raised when a dataframe/array-like object has an empty shape."""

    ...
