from functools import partial, wraps
from typing import Callable

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
    Decorates a decorator function in order to check whether or not it gets called with
    parens, and therefore deal with its optional arguments.

    Arguments:
        decorator: decorator to wrap

    Usage:

    ```python
    # `decorator` called default params, and without parens
    @decorator
    def func(*func_args, **func_kwargs):
        pass

    # `decorator` called with custom params, of course with parens
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
