from typing import Callable, Any
from functools import wraps, partial
from datetime import datetime

import inspect
import os
import pickle
import time

import chime

from ._core import add_partial
from ._logging_fn import LOGGING_FN


@add_partial
def call_counter(
    func: Callable = None,
    seed: int = 0,
    log_counter: bool = False,
    logging_fn: Callable = LOGGING_FN,
) -> Callable:
    """
    Stores how many times many times a function has been called in the `_calls` attribute

    Arguments:
        func: function to decorate
        seed: counter start, default=0
        log_counter: whether display count number, default=False
        logging_fn: function to use to display log_counter

    Usage:

    ```python
    from deczoo import call_counter

    @call_counter
    def add(a, b): return a+b

    for _ in range(3):
        add(1,2)

    add._calls
    3
    ```
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Callable:
        wrapper._calls += 1

        if log_counter:
            logging_fn(f"{func.__name__} called {wrapper._calls} times")

        return func(*args, **kwargs)

    wrapper._calls = seed

    return wrapper


@add_partial
def catch(
    func: Callable = None,
    return_on_exception: Any = None,
    raise_on_execption: Any = None,
    logging_fn: Callable = LOGGING_FN,
) -> Callable:
    """
    Wraps a function in a try-except block,
    potentially prevent exception to be raised or raises custom exception

    Arguments:
        func: function to decorate
        raise_on_exception: error to raise on exception
        return_on_exception: value to return on exception
        logging_fn: log function (e.g. print, logger.info, console.log), defualt=console.log

    ```python
    from deczoo import catch

    @catch(return_on_exception=-999)
    def add(a, b): return a+b

    add(1, 2)
    3

    add(1, "a")
    -999
    ```
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Callable:
        try:
            return func(*args, **kwargs)

        except Exception as e:

            if return_on_exception is not None:
                logging_fn(f"Failed with error {e}, returning {return_on_exception}")
                return return_on_exception

            elif raise_on_execption is not None:
                logging_fn(f"Failed with error {e}")
                raise raise_on_execption

            else:
                logging_fn(f"Failed with error {e}")
                raise e

    return wrapper


@add_partial
def check_args(func: Callable = None, **rules) -> Callable:
    """
    Checks that arguments passed to func satisfy given rules

    Arguments:
        func: function to be decorated
        rules: rules to be satisfied

    Usage:

    ```python
    from deczoo import check_args

    @check_args(a=lambda t: t>0)
    def add(a, b): return a+b

    add(1,2)
    3

    add(-2, 2)
    ValueError: Argument a doesn't satisfy its rule
    ```
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Callable:

        func_args = inspect.signature(func).bind(*args, **kwargs).arguments

        for k, v in func_args.items():
            rule = rules.get(k)

            if rule is not None:

                if not rule(v):
                    raise ValueError(f"Argument {k} doesn't satisfy its rule")

        res = func(*args, **kwargs)
        return res

    return wrapper


@add_partial
def chime_on_end(func: Callable = None, theme: str = None) -> Callable:
    """
    Notify with chime sound on function end

    Arguments:
        - func: function to decorate
        - theme: chime theme to use

    Usage:

    ```python
    from deczoo import chime_on_end

    @chime_on_end
    def add(a, b): return a+b

    _ = add(1, 2)
    > you should hear a sound now!
    ```
    """
    chime.theme(theme)

    @wraps(func)
    def wrapper(*args, **kwargs) -> Callable:

        try:
            res = func(*args, **kwargs)
            chime.success()
            return res

        except Exception as e:
            chime.error()
            raise e

    return wrapper


@add_partial
def dump_result(
    func: Callable = None,
    result_path: str = "results",
    include_args: bool = False,
    include_time: bool = True,
    time_fmt: str = "%Y%m%d_%H%M%S",
    logging_fn: Callable = LOGGING_FN,
) -> Callable:
    """
    Saves function result in a pickle file

    Arguments:
        func: function to decorate
        result_path: path to folder where to save the result, default="results"
        include_args: whether to add arguments the function run with in the filename, default=False
        include_time: whether to add when the function run in the filename, default=True
        time_fmt: time format, used only if include_time=True, default="%Y%m%d_%H%M%S"
        logging_fn: log function (e.g. print, logger.info, console.log), defualt=console.log

    Usage:

    ```python
    from deczoo import dump_result

    @dump_result
    def add(a, b): return a+b

    _ = add(1, 2)
    > will save the result in results/add_%Y%m%d_%H%M%S.pickle
    ```
    """
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    @wraps(func)
    def wrapper(*args, **kwargs) -> Callable:

        res = func(*args, **kwargs)

        func_args_str = ""
        func_time_str = ""

        if include_args:
            func_args = inspect.signature(func).bind(*args, **kwargs).arguments
            func_args_str = "_" + "_".join(f"{v}" for k, v in func_args.items())

        if include_time:
            func_time_str = f"_{datetime.now().strftime(time_fmt)}"

        _file = f"{result_path}/{func.__name__}{func_args_str}{func_time_str}.pickle"

        with open(_file, "wb") as outp:
            pickle.dump(res, outp, pickle.HIGHEST_PROTOCOL)
            logging_fn(f"Result of {func.__name__} saved at {_file}")

        return res

    return wrapper


@add_partial
def log(
    func: Callable = None,
    log_time: bool = True,
    log_args: bool = True,
    log_error: bool = True,
    logging_fn: Callable = LOGGING_FN,
) -> Callable:
    """
    Tracks function time taken, arguments and errors

    Arguments:
        func: function to decorate
        log_time: whether to log time taken or not, default=True
        log_args: whether to log arguments or not, default=True
        log_error: whether to log error or not, default=True
        logging_fn: log function (e.g. print, logger.info, console.log), default=print

    Usage:

    ```python
    from deczoo import log

    @log
    def add(a, b): return a+b

    _ = add(1, 2)
    add args=(a=1, b=2) time=0:00:00.000111
    ```
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Callable:

        tic = datetime.now()

        if log_args:

            func_args = inspect.signature(func).bind(*args, **kwargs).arguments
            func_args_str = ", ".join(f"{k}={v}" for k, v in func_args.items())

            optional_strings = [f"args=({func_args_str})"]

        else:
            optional_strings = []

        try:
            res = func(*args, **kwargs)
            toc = datetime.now()
            optional_strings += [
                f"time={toc- tic}" if log_time else None,
            ]

            return res

        except Exception as e:

            toc = datetime.now()
            optional_strings += [
                f"time={toc - tic}" if log_time else None,
                "Failed" + (f" with error: {e}" if log_error else ""),
            ]
            raise e

        finally:
            log_string = (
                f"{func.__name__} {' '.join([s for s in optional_strings if s])}"
            )
            logging_fn(log_string)

    return wrapper


timer = partial(log, log_time=True, log_args=False, log_error=False)


@add_partial
def retry(
    func: Callable = None,
    n_tries: int = 1,
    delay: float = 0.0,
    logging_fn: Callable = LOGGING_FN,
) -> Callable:
    """
    Decorates a function with a retry block

    Arguments:
        func: function to decorate
        n_tries: max number of attempts to try, default=1
        delay: time to wait before a retry, default=0
        logging_fn: log function (e.g. print, logger.info, console.log), defualt=console.log

    Usage:

    ```python
    from deczoo import retry

    @retry(n_tries=2, delay=1.)
    def add(a, b): return a+b

    _ = add(1, 2)
    Attempt 1/2: Successed

    _ = add(1, "a")
    Attempt 1/2: Failed with error: unsupported operand type(s) for +: 'int' and 'str'
    Attempt 2/2: Failed with error: unsupported operand type(s) for +: 'int' and 'str'
    ```
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Callable:

        attempt = 0

        while attempt < n_tries:

            try:
                res = func(*args, **kwargs)
                logging_fn(f"Attempt {attempt+1}/{n_tries}: Successed")
                return res

            except Exception as e:
                logging_fn(f"Attempt {attempt+1}/{n_tries}: Failed with error: {e}")

                time.sleep(delay)
                attempt += 1
                if attempt == n_tries:
                    raise e

    return wrapper