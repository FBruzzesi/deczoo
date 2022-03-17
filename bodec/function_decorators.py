from typing import Callable, Any
from functools import wraps
from datetime import datetime
import inspect
import time

from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({"good": "bold green", "bad": "bold red"})
console = Console(theme=custom_theme)


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

    Arguments:
        - func: function to decorate
        - raise_on_exception: error to raise on exception
        - return_on_exception: value to return on exception
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
def retry(
    func: Callable = None,
    n_tries: int = 1,
    delay: float = 0.0,
    logging_fn: Callable = console.log,
) -> Callable:
    """
    Decorates a function with a retry block

    Arguments:
        - func: function to decorate
        - n_tries: max number of attempts to try, default=1
        - delay: time to wait before a retry, default=0
        - logging_fn: log function (e.g. print, logger.info, console.log), defualt=console.log
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Callable:
        attempt = 0

        while attempt < n_tries:
            msg = f" Attempt {attempt+1} out of {n_tries}"

            try:
                res = func(*args, **kwargs)
                logging_fn(":heavy_check_mark:" + msg, style="good")
                return res

            except Exception as e:
                logging_fn(":x:" + msg, style="bad")

                time.sleep(delay)
                attempt += 1
                if attempt == n_tries:
                    raise e

    return wrapper


@add_partial
def log(
    func: Callable = None,
    log_time: bool = True,
    log_args: bool = True,
    log_error: bool = True,
    logging_fn: Callable = console.log,
):
    """
    Arguments:
        - func: function to decorate
        - log_time: whether to log time taken or not, default=True
        - log_args: whether to log arguments or not, default=True
        - log_error: whether to log error or not, default=True
        - logging_fn: log function (e.g. print, logger.info, console.log), default=console.log
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Callable:

        tic = datetime.now()
        optional_strings = []
        try:
            res = func(*args, **kwargs)

            optional_strings = [
                f"time={datetime.now() - tic}" if log_time else None,
            ]
            return res

        except Exception as e:
            optional_strings = [
                f"time={datetime.now() - tic}" if log_time else None,
                "FAILED" + (f" with error: {e}" if log_error else ""),
            ]
            raise e

        finally:
            combined = " ".join([s for s in optional_strings if s])

            if log_args:

                func_args = inspect.signature(func).bind(*args, **kwargs).arguments
                func_args_str = "".join(
                    ", {} = {!r}".format(*item) for item in list(func_args.items())[1:]
                )
                logging_fn(
                    f"[{func.__name__}(df{func_args_str})] " + combined,
                )

            else:
                logging_fn(
                    f"[{func.__name__}]" + combined,
                )

    return wrapper


def timer(func):
    """Times func"""
    pass


def call_counter(func):
    """Counts how many times func is called"""
    pass
