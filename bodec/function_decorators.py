from typing import Callable, Any
from functools import wraps
import time

from .core import add_partial


@add_partial
def catch(
    func: Callable = None,
    return_on_exception: Any = None,
    raise_on_execption: Any = None,
) -> Callable:
    """
    Wraps a function in a try-except block,
    potentially prevent exception to be raised or raises custom exception
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Callable:
        try:
            return func(*args, **kwargs)

        except Exception as e:
            if return_on_exception is not None:
                return return_on_exception
            elif raise_on_execption is not None:
                raise raise_on_execption
            else:
                raise e

    return wrapper


@add_partial
def retry(func):
    """Retries func n times, eventually raises exception"""
    pass


def timer(func):
    """Times func"""
    pass


def call_counter(func):
    """Counts how many times func is called"""
    pass
