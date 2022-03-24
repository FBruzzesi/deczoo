from typing import Callable
from functools import partial, wraps

try:
    from rich.console import Console
    from rich.theme import Theme

    custom_theme = Theme({"good": "bold green", "bad": "bold red"})
    console = Console(theme=custom_theme)

    LOGGING_FN = console.print

except:
    LOGGING_FN = print


def check_parens(decorator: Callable) -> Callable:
    """
    Decorates a decorator function in order to check if it gets called with or without parens, and therefore deal with its optional arguments.
    In such a way decorator can be called both with or without params:

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


'''
def set_logging_fn(func: Callable = None):
    """
    Set the global value of logging_fn.

    Argument:
        func: The change will be switched if a valid name is provided. The current theme is
            returned if `None`.
    Raises:
        ValueError: If the theme is unknown.
    """

    global LOGGING_FN

    if func is None:
        return LOGGING_FN
    elif not isinstance(func, Callable):
        raise ValueError("func is not callable, please provide a callable logging function")
    else:
        LOGGING_FN = func
'''
