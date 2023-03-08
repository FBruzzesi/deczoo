import inspect
import resource
import signal
import time
from enum import Enum
from functools import partial, wraps
from typing import Any, Callable, Optional, Union

import chime

from ._base_notifier import BaseNotifier
from ._utils import LOGGING_FN, check_parens


@check_parens
def call_counter(
    func: Optional[Callable] = None,
    seed: int = 0,
    log_counter: bool = False,
    logging_fn: Callable = LOGGING_FN,
) -> Callable:
    """
    Counts how many times a function has been called in the `_calls` attribute

    Arguments:
        func: function to decorate
        seed: counter start
        log_counter: whether display count number
        logging_fn: log function (e.g. print, logger.info, rich console.print)

    Raises:
        ValueError: if seed is not an int

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

    if not isinstance(seed, int):
        raise TypeError("`seed` argument must be an int")

    @wraps(func)  # type: ignore
    def wrapper(*args, **kwargs):

        wrapper._calls += 1

        if log_counter:
            logging_fn(f"{func.__name__} called {wrapper._calls} times")

        return func(*args, **kwargs)

    # set counter dynamically
    wrapper._calls = seed  # type: ignore

    return wrapper


@check_parens
def catch(
    func: Optional[Callable] = None,
    return_on_exception: Optional[Any] = None,
    raise_on_exception: Optional[Any] = None,
    logging_fn: Callable = LOGGING_FN,
) -> Callable:
    """
    Wraps a function in a try-except block,
    potentially prevent exception to be raised or raises custom exception

    Arguments:
        func: function to decorate
        return_on_exception: value to return on exception
        raise_on_exception: error to raise on exception
        logging_fn: log function (e.g. print, logger.info, rich console.print)

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

    @wraps(func)  # type: ignore
    def wrapper(*args, **kwargs):

        try:
            return func(*args, **kwargs)

        except Exception as e:

            if return_on_exception is not None:
                logging_fn(f"Failed with error {e}, returning {return_on_exception}")
                return return_on_exception

            elif raise_on_exception is not None:
                logging_fn(f"Failed with error {e}")
                raise raise_on_exception

            else:
                logging_fn(f"Failed with error {e}")
                raise e

    return wrapper


@check_parens
def check_args(
    func: Optional[Callable] = None, **rules: Callable[[Any], bool]
) -> Callable:
    """
    Checks that function arguments satisfy given rules, if not raises a ValueError

    Arguments:
        func: function to decorate
        rules: rules to be satisfied, each rule is a function that takes the argument value
            and returns a boolean

    Usage:

    ```python
    from deczoo import check_args

    @check_args(a=lambda t: t>0)
    def add(a, b): return a+b

    add(1,2)
    3

    add(-2, 2)
    # ValueError: Argument a doesn't satisfy its rule
    ```
    """

    @wraps(func)  # type: ignore
    def wrapper(*args, **kwargs) -> Callable:

        func_args = inspect.signature(func).bind(*args, **kwargs).arguments  # type: ignore

        for k, v in func_args.items():
            rule = rules.get(k)

            if rule is not None:

                if not rule(v):
                    raise ValueError(f"Argument {k} doesn't satisfy its rule")

        res = func(*args, **kwargs)  # type: ignore
        return res

    return wrapper


@check_parens
def chime_on_end(
    func: Optional[Callable] = None, theme: Optional[str] = None
) -> Callable:
    """
    Notify with chime sound on function end

    Arguments:
        func: function to decorate
        theme: chime theme to use

    Usage:

    ```python
    from deczoo import chime_on_end

    @chime_on_end
    def add(a, b): return a+b

    _ = add(1, 2)
    # you should hear a sound now!
    ```
    """
    chime.theme(theme)

    @wraps(func)  # type: ignore
    def wrapper(*args, **kwargs):

        try:
            res = func(*args, **kwargs)
            chime.success()
            return res

        except Exception as e:
            chime.error()
            raise e

    return wrapper


@check_parens
def log(
    func: Optional[Callable] = None,
    log_time: bool = True,
    log_args: bool = True,
    log_error: bool = True,
    log_file: Optional[str] = None,
    logging_fn: Callable = LOGGING_FN,
) -> Callable:
    """
    Tracks function time taken, arguments and errors

    Arguments:
        func: function to decorate
        log_time: whether or not to log time taken
        log_args: whether or not to log arguments
        log_error: whether or not to log error
        log_file: filepath where to write log
        logging_fn: log function (e.g. print, logger.info, rich console.print)

    Usage:

    ```python
    from deczoo import log

    @log
    def add(a, b): return a+b

    _ = add(1, 2)
    # add args=(a=1, b=2) time=0:00:00.000111
    ```
    """

    @wraps(func)  # type: ignore
    def wrapper(*args, **kwargs):

        tic = time.perf_counter()

        if log_args:

            func_args = inspect.signature(func).bind(*args, **kwargs).arguments
            func_args_str = ", ".join(f"{k}={v}" for k, v in func_args.items())

            optional_strings = [f"args=({func_args_str})"]

        else:
            optional_strings = []

        try:
            res = func(*args, **kwargs)
            toc = time.perf_counter()
            optional_strings += [
                f"time={toc - tic}" if log_time else None,
            ]

            return res

        except Exception as e:

            toc = time.perf_counter()
            optional_strings += [
                f"time={toc - tic}" if log_time else None,
                "Failed" + (f" with error: {e}" if log_error else ""),
            ]
            raise e

        finally:
            log_string = f"{func.__name__} {' '.join([s for s in optional_strings if s])}"
            logging_fn(log_string)

            if log_file is not None:

                with open(log_file, "a") as f:
                    f.write(f"{tic} {log_string}\n")

    return wrapper


timer = partial(log, log_time=True, log_args=False, log_error=False)


def _get_free_memory() -> int:
    """
    Computes machine free memory via /proc/meminfo (linux only)
    !Warning: Currently supports linux only
    """

    with open("/proc/meminfo", "r") as mem:
        free_memory = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) in ("MemFree:", "Buffers:", "Cached:"):
                free_memory += int(sline[1])
    return free_memory


@check_parens
def memory_limit(
    func: Optional[Callable] = None,
    percentage: float = 0.99,
    logging_fn: Callable = LOGGING_FN,
) -> Callable:
    """
    Sets a memory limit for a function

    Arguments:
        func: function to decorate
        percentage: percentage of the currently available memory to use
        logging_fn: log function (e.g. print, logger.info, rich console.print)

    Usage:

    ```python
    from deczoo import memory_limit

    # Running on WSL2 with 12 Gb RAM

    @memory_limit(percentage=0.2)
    def limited():
        for i in list(range(10 ** 8)):
            _ = 1 + 1
        return "done"

    def unlimited():
        for i in list(range(10 ** 8)):
            _ = 1 + 1
        return "done"

    limited()
    # MemoryError: Reached memory limit

    unlimited()
    done
    ```
    """
    if not isinstance(percentage, float):
        raise TypeError("percentage should be a float")

    if not 0 <= percentage <= 1:
        raise ValueError("percentage should be between 0 and 1")

    @wraps(func)  # type: ignore
    def wrapper(*args, **kwargs):

        _, hard = resource.getrlimit(resource.RLIMIT_AS)
        free_memory = _get_free_memory() * 1024

        logging_fn(
            f"Setting memory limit for {func.__name__} to {int(free_memory * percentage)}"
        )

        resource.setrlimit(resource.RLIMIT_AS, (int(free_memory * percentage), hard))

        try:
            return func(*args, **kwargs)

        except MemoryError:
            raise MemoryError("Reached memory limit")

        finally:
            resource.setrlimit(resource.RLIMIT_AS, (int(free_memory), hard))

    return wrapper


@check_parens
def notify_on_end(func: Callable = None, notifier: BaseNotifier = None) -> Callable:
    """
    Notify when func has finished running using the notifier `notify` method.
    `notifier` object should inherit from BaseNotifier

    Arguments:
        func: function to decorate
        notifier: instance of a Notifier that implements `notify` method

    Usage:

    ```python
    from deczoo import notify_on_end
    from deczoo._base_notifier import BaseNotifier

    class DummyNotifier(BaseNotifier):
        def notify(self):
            print("Function has finished")

    notifier = DummyNotifier()
    @notify_on_end(notifier=notifier)
    def add(a, b): return a + b

    _ = add(1, 2)
    # Function has finished
    ```
    """

    @wraps(func)  # type: ignore
    def wrapper(*args, **kwargs):

        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            notifier.notify()

    return wrapper


@check_parens
def retry(
    func: Optional[Callable] = None,
    n_tries: int = 3,
    delay: float = 0.0,
    logging_fn: Callable = LOGGING_FN,
) -> Callable:
    """
    Wraps a function with a retry block

    Arguments:
        func: function to decorate
        n_tries: max number of attempts to try
        delay: time to wait before a retry
        logging_fn: log function (e.g. print, logger.info, rich console.print)

    Usage:

    ```python
    from deczoo import retry

    @retry(n_tries=2, delay=1.)
    def add(a, b): return a+b

    _ = add(1, 2)
    # Attempt 1/2: Successed

    _ = add(1, "a")
    # Attempt 1/2: Failed with error: unsupported operand type(s) for +: 'int' and 'str'
    # Attempt 2/2: Failed with error: unsupported operand type(s) for +: 'int' and 'str'
    ```
    """
    if not isinstance(n_tries, int) or n_tries < 1:
        raise ValueError("`n_tries` should be a positive integer")

    if not isinstance(delay, (int, float)) or delay < 0:
        raise ValueError("`delay` should be a positive number")

    @wraps(func)  # type: ignore
    def wrapper(*args, **kwargs):

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


@check_parens
def timeout(
    func: Optional[Callable] = None,
    time_limit: Optional[int] = None,
    signal_handler: Optional[Callable] = None,
    signum: Union[int, Enum] = signal.SIGALRM,
    logging_fn: Callable = LOGGING_FN,
) -> Callable:
    """
    Sets a time limit to a function, terminates the process if it hasn't finished within
    such time limit.

    Remark that it uses the signal library (https://docs.python.org/3/library/signal.html)
    which fully supported only on UNIX.

    Arguments:
        func: function to decorate
        time_limit: max time (in seconds) for function to run, 0 means no time limit
        signal_handler: custom signal handler
        signum: signal number to be used, default=signal.SIGALRM (14)
        logging_fn: log function (e.g. print, logger.info, rich console.print)

    Usage:

    ```python
    import time
    from deczoo import timeout

    @timeout(time_limit=3)
    def add(a, b):
        time.sleep(2)
        return a+b

    add(1, 2)
    3

    @timeout(time_limit=1)
    def add(a, b):
        time.sleep(2)
        return a+b

    add(1, 2)
    # Exception: Reached time limit, terminating add
    ```
    """

    if not isinstance(time_limit, (int, float)) or time_limit < 0:
        raise ValueError("`time_limit` should be a positive number")

    if signal_handler is None:

        def signal_handler(signum, frame):
            raise Exception(f"Reached time limit, terminating {func.__name__}")

        signal.signal(signum, signal_handler)  # type: ignore

    @wraps(func)  # type: ignore
    def wrapper(*args, **kwargs):

        signal.alarm(time_limit)

        try:
            res = func(*args, **kwargs)
            signal.alarm(0)
            return res
        except Exception as e:
            raise e

    return wrapper
