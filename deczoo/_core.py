from typing import Callable
from functools import partial


def add_partial(decorator: Callable) -> Callable:
    """
    Decorates a decorator function in order to deal with its optional arguments
    In such a way decorator can be called both as:

    ```python
    # `decorator` called default params
    @decorator
    def func(*func_args, **func_kwargs):
        pass

    # `decorator` called with custom params
    @decorator(*args, **kwargs)
    def func(*func_args, **func_kwargs):
        pass
    ```
    """

    def wrapper(func: Callable = None, *args, **kwargs) -> Callable:

        if func is None:
            return partial(decorator, *args, **kwargs)
        else:
            return decorator(func, *args, **kwargs)

    return wrapper