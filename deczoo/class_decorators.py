from typing import Callable
from datetime import datetime

from .core import add_partial


@add_partial
def birthday(cls) -> Callable:
    """Add birthday to class instance"""

    def wrapper(*args, **kwargs):

        instance = cls(*args, **kwargs)
        instance._birthday = datetime.now()

        return instance

    return wrapper


@add_partial
def instance_counter(
    cls, seed: int = 0, log_counter: bool = False, logging_fn: Callable = print
):

    """Counts how many times a class in instantiated"""

    pass
