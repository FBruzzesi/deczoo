import sys
from functools import partial, wraps
from typing import Callable, Protocol, Tuple, TypeVar, Union, runtime_checkable

if sys.version_info >= (3, 10):
    from typing import ParamSpec, TypeAlias
else:
    from typing_extensions import ParamSpec, TypeAlias

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

PS = ParamSpec("PS")
R = TypeVar("R")
F: TypeAlias = Callable[PS, R]

# DPS = ParamSpec("DPS")
# DecoratorType: TypeAlias = Callable[[F, DPS.args, DPS.kwargs], F]


def check_parens(decorator: F) -> F:
    """Check whether or not a decorator function gets called with parens:

    - If called with parens, the decorator is called without the function as the first argument, but necessarely with
        decorator keyword arguments.
    - If called without parens, the decorator is called with the function as the first argument, and the decorator's
        default arguments.

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
    def wrapper(func: Union[F, None] = None, *args: PS.args, **kwargs: PS.kwargs) -> F:
        if func is None:
            return partial(decorator, *args, **kwargs)
        else:
            return decorator(func, *args, **kwargs)

    return wrapper


def _get_free_memory() -> int:
    """Computes machine free memory via `/proc/meminfo` file (linux only).

    !!! warning
        This functionality is supported on unix-based systems only!
    """

    with open("/proc/meminfo", "r") as mem:
        free_memory = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) in ("MemFree:", "Buffers:", "Cached:"):
                free_memory += int(sline[1])
    return free_memory


@runtime_checkable
class SupportShape(Protocol):
    """Protocol for objects that have a `.shape()` attribute. In this context, a dataframe or array like object."""

    @property
    def shape(self: Self) -> Tuple[int, ...]:
        ...


class EmptyShapeError(Exception):
    """Exception raised when a dataframe/array-like object has an empty shape."""

    ...


LoggerType: TypeAlias = Callable[[str], None]
LOGGING_FN: LoggerType

try:
    from rich.console import Console
    from rich.theme import Theme

    custom_theme = Theme({"good": "bold green", "bad": "bold red"})
    console = Console(theme=custom_theme)

    LOGGING_FN = console.log

except ImportError:
    LOGGING_FN = print
