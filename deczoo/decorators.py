import inspect
import resource
import signal
import time
from enum import Enum
from functools import partial, wraps
from itertools import zip_longest
from pathlib import Path
from typing import Any, Callable, Literal, Optional, Sequence, Tuple, Union

from ._base_notifier import BaseNotifier
from ._utils import LOGGING_FN, EmptyShapeError, HasShape, _get_free_memory, check_parens


@check_parens
def call_counter(
    func: Optional[Callable] = None,
    seed: int = 0,
    log_counter: bool = True,
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
        TypeError: if `seed` is not an int, or `log_counter` is not a bool

    Returns:
        decorated function

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

    if not isinstance(log_counter, bool):
        raise TypeError("`log_counter` argument must be a bool")

    if not callable(logging_fn):
        raise TypeError("`logging_fn` argument must be a callable")

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
    Wraps a function in a try-except block, potentially prevent exception to be raised by
    returning a given value or raises custom exception.

    Remark that if both `return_on_exception` and `raise_on_exception` are provided,
    `return_on_exception` will be used.

    Arguments:
        func: function to decorate
        return_on_exception: value to return on exception
        raise_on_exception: error to raise on exception
        logging_fn: log function (e.g. print, logger.info, rich console.print)

    Returns:
        decorated function

    Raises:
        TypeError: if `logging_fn` is not a callable

    Usage:
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

    if not callable(logging_fn):
        raise TypeError("`logging_fn` argument must be a callable")

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
        rules: rules to be satisfied, each rule is a function that takes the argument
            value and returns a boolean

    Returns:
        decorated function

    Raises:
        ValueError: if any rule is not a callable
        ValueError: if decorated function argument doesn't satisfy its rule

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
    if not all(callable(rule) for rule in rules.values()):
        raise ValueError("All rules must be callable")

    @wraps(func)  # type: ignore
    def wrapper(*args, **kwargs) -> Callable:

        func_args = (
            inspect.signature(func).bind(*args, **kwargs).arguments  # type: ignore
        )

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
    func: Optional[Callable] = None, theme: Optional[str] = "mario"
) -> Callable:
    """
    Notify with [chime](https://github.com/MaxHalford/chime) sound on when function
    ends successfully or fails.

    Arguments:
        func: function to decorate
        theme: chime theme to use

    Returns:
        decorated function

    Usage:
    ```python
    from deczoo import chime_on_end

    @chime_on_end
    def add(a, b): return a+b

    _ = add(1, 2)
    # you should hear a sound now!
    ```
    """
    import chime

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
    log_file: Optional[Union[Path, str]] = None,
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

    Returns:
        decorated function with logging capabilities

    Raises:
        TypeError: if `log_time`, `log_args` or `log_error` are not `bool` or `log_file` \
        is not `None`, `str` or `Path`

    Usage:
    ```python
    from deczoo import log

    @log
    def add(a, b): return a+b

    _ = add(1, 2)
    # add args=(a=1, b=2) time=0:00:00.000111
    ```
    """

    if not all(isinstance(x, bool) for x in [log_time, log_args, log_error]):
        raise TypeError("`log_time`, `log_args` and `log_error` must be bool")

    if log_file is not None and not isinstance(log_file, (str, Path)):
        raise TypeError("`log_file` must be either None, str or Path")

    if not callable(logging_fn):
        raise TypeError("`logging_fn` must be callable")

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


@check_parens
def memory_limit(
    func: Optional[Callable] = None,
    percentage: float = 0.99,
    logging_fn: Callable = LOGGING_FN,
) -> Callable:
    """
    Sets a memory limit while running a function.

    **Warning**: This decorator is supported on unix-based systems only!

    Arguments:
        func: function to decorate
        percentage: percentage of the currently available memory to use
        logging_fn: log function (e.g. print, logger.info, rich console.print)

    Raises:
        TypeError: if `percentage` is not a `float`
        ValueError: if `percentage` is not between 0 and 1
        MemoryError: if memory limit is reached when decorated function is called

    Returns:
        decorated function

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
        raise TypeError("`percentage` should be a float")

    if not 0.0 <= percentage <= 1.0:
        raise ValueError("`percentage` should be between 0 and 1")

    if not callable(logging_fn):
        raise TypeError("`logging_fn` should be a callable")

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

    Returns:
        decorated function

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
    if not isinstance(notifier, BaseNotifier):
        raise TypeError("`notifier` should be an instance of a BaseNotifier")

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

    Raises:
        ValueError: if `n_tries` is not a positive integer, `delay` is not a \
            positive number, or `logging_fn` is not a callable

    Returns:
        decorated function

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

    if not callable(logging_fn):
        raise TypeError("`logging_fn` should be a callable")

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
def shape_tracker(
    func: Optional[Callable[[HasShape, Sequence[Any]], HasShape]] = None,
    shape_in: bool = False,
    shape_out: bool = True,
    shape_delta: bool = False,
    raise_if_empty: bool = True,
    arg_to_track: Optional[Union[int, str]] = 0,
    logging_fn: Callable = LOGGING_FN,
) -> Callable:
    """
    Tracks the shape of a dataframe/array-like object.
    It's possible to track input, output shapes, delta from input and output, and raise
    an error if resulting output is empty.

    Parameters:
        func: function to decorate
        shape_in: track input shape
        shape_out: track output shape
        shape_delta: track shape delta between input and output
        raise_if_empty: raise error if output is empty
        arg_to_track: index or name of the argument to track
        logging_fn: log function (e.g. print, logger.info, rich console.print)

    Returns:
        decorated function

    Raises:
        TypeError: if any of the parameters is not of the correct type
        EmptyShapeError: if decorated function output is empty and `raise_if_empty` is\
            `True`

    Usage:
    ```python
    import numpy as np
    from deczoo import shape_tracker

    @shape_tracker(shape_in=True, shape_out=True, shape_delta=True)
    def n_vstack(a: np.ndarray, n: int) -> np.ndarray:
        return np.vstack(n*[a])

    a = np.random.randn(10, 20, 30)
    _ = n_vstack(a, 3)

    # Input shape: (10, 20, 30)
    # Output shape: (30, 20, 30)
    # Shape delta: (-20, 0, 0)
    ```
    Now if the array to track is not the first argument, we can explicitely specify the
    index of the argument to track using `idx_to_track` parameter:

    ```python
    import numpy as np
    from deczoo import shape_tracker

    @shape_tracker(shape_in=True, shape_out=True, shape_delta=True, idx_to_track=1)
    def n_vstack(n: int, a: np.ndarray) -> np.ndarray:
        return np.vstack(n*[a])

    a = np.random.randn(10, 20, 30)
    _ = n_vstack(n=3, a=a)

    # Input shape: (10, 20, 30)
    # Output shape: (30, 20, 30)
    # Shape delta: (-20, 0, 0)
    ```
    """
    if not isinstance(shape_in, bool):
        raise TypeError("shape_in should be a boolean")

    if not isinstance(shape_out, bool):
        raise TypeError("shape_out should be a boolean")

    if not isinstance(shape_delta, bool):
        raise TypeError("shape_delta should be a boolean")

    if not isinstance(raise_if_empty, bool):
        raise TypeError("raise_if_empty should be a boolean")

    if (not isinstance(arg_to_track, (str, int))) or (
        isinstance(arg_to_track, int) and arg_to_track < 0
    ):
        raise TypeError("arg_to_track should be a string or a positive integer")

    @wraps(func)  # type: ignore
    def wrapper(*args: Any, **kwargs: Any) -> HasShape:

        func_args = (
            inspect.signature(func).bind(*args, **kwargs).arguments  # type: ignore
        )

        if isinstance(arg_to_track, int) and arg_to_track >= 0:
            _arg_name, _arg_value = tuple(func_args.items())[arg_to_track]
        elif isinstance(arg_to_track, str):
            _arg_name, _arg_value = arg_to_track, func_args[arg_to_track]
        else:
            raise ValueError("arg_to_track should be a string or a positive integer")

        if shape_in:
            logging_fn(f"Input: {_arg_name} has shape {_arg_value.shape}")

        res = func(*args, **kwargs)  # type: ignore

        output_shape = res.shape

        if shape_out:
            logging_fn(f"Output: result has shape {output_shape}")

        if shape_delta:
            input_shape = _arg_value.shape
            delta = tuple(
                d1 - d2 for d1, d2 in zip_longest(input_shape, output_shape, fillvalue=0)
            )

            logging_fn(f"Shape delta: {delta}")

        if raise_if_empty and output_shape[0] == 0:
            raise EmptyShapeError(f"Result from {func.__name__} is empty")  # type: ignore

        return res

    return wrapper


@check_parens
def multi_shape_tracker(
    func: Optional[Callable[[HasShape, Sequence[Any]], Tuple[HasShape, ...]]] = None,
    shapes_in: Optional[Union[str, int, Sequence[str], Sequence[int]]] = None,
    shapes_out: Optional[Union[int, Sequence[int], Literal["all"]]] = "all",
    raise_if_empty: Optional[Literal["any", "all"]] = "any",
    logging_fn: Callable = LOGGING_FN,
) -> Callable:
    """
    Tracks the shape(s) of a dataframe/array-like objects both in input and output of
    a given function.

    Arguments:
        func: function to decorate
        shapes_in: sequence of argument positions OR argument names to track
        shapes_out: sequence of argument positions to track, or "all" to track all
        raise_if_empty: raise error if output is empty (strategy: "any" or "all")
        logging_fn: log function (e.g. print, logger.info, rich console.print)

    Returns:
        decorated function

    Raises:
        TypeError: if any of the parameters is not of the correct type
        EmptyShapeError: if decorated function output is empty and `raise_if_empty` is\
            `all` or `any`

    Usage:
    ```python
    import numpy as np
    from deczoo import multi_shape_tracker

    @multi_shape_tracker(shapes_in=(0,1), shapes_out="all")
    def add_multi(a: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        return a + b, a * b

    a = np.random.randn(10, 20, 30)
    b = np.random.randn(10, 20, 30)
    _ = add_multi(a, b)

    # Input shapes: a.shape=(10, 20, 30), b.shape=(10, 20, 30)
    # Output shapes: (10, 20, 30), (10, 20, 30)
    ```
    """

    @wraps(func)  # type: ignore
    def wrapper(*args: Any, **kwargs: Any) -> HasShape:

        func_args = (
            inspect.signature(func).bind(*args, **kwargs).arguments  # type: ignore
        )
        # parse shapes_in
        # case: str
        if isinstance(shapes_in, str):
            _arg_names, _arg_values = shapes_in, func_args[shapes_in]

        # case: int
        elif isinstance(shapes_in, int) and shapes_in >= 0:
            _arg_names, _arg_values = tuple(
                x for x in tuple(func_args.items())[shapes_in]
            )

        # case: sequence
        elif isinstance(shapes_in, Sequence):

            # case: sequence of str's
            if all(isinstance(x, str) for x in shapes_in):
                _arg_names, _arg_values = tuple(shapes_in), tuple(  # type: ignore
                    func_args[x] for x in shapes_in  # type: ignore
                )

            # case: sequence of positive int's
            elif all(isinstance(x, int) and x >= 0 for x in shapes_in):
                _arg_names, _arg_values = zip(  # type: ignore
                    *(tuple(func_args.items())[x] for x in shapes_in)  # type: ignore
                )

            # case: sequence of something else! (raise error)
            else:
                raise TypeError("shapes_in values must all be str or positive int")

        # case: None
        elif shapes_in is None:
            pass

        # case: something else, not in Union[int, str, Sequence[int], Sequence[str], None]
        else:
            raise TypeError(
                "shapes_in must be either a str, a positive int, a sequence of str's, \
                    a sequence of positive int's or None"
            )

        if shapes_in is not None:

            logging_fn(
                "Input shapes: "
                + " ".join(
                    f"{k}.shape={v.shape}" for k, v in zip(_arg_names, _arg_values)
                )
            )

        # finally run the function!
        orig_res = func(*args, **kwargs)  # type: ignore

        # Check if the function returns a single value or a tuple
        res = (orig_res,) if not isinstance(orig_res, Sequence) else orig_res

        # parse shapes_out
        # case: positive int
        if isinstance(shapes_out, int) and shapes_out >= 0:
            _res_shapes = (res[shapes_out].shape,)

        # case: sequence of positive int's
        elif isinstance(shapes_out, Sequence) and all(
            isinstance(x, int) and x >= 0 for x in shapes_out
        ):
            _res_shapes = tuple(res[x].shape for x in shapes_out)  # type: ignore

        # case: "all"
        elif shapes_out == "all":
            _res_shapes = tuple(x.shape for x in res)  # type: ignore

        # case: None
        elif shapes_out is None:
            pass

        # case: something else, not in Union[int, Sequence[int], Literal["all"], None]
        else:
            raise TypeError(
                "shapes_out must be positive int, sequence of positive int or 'all'"
            )

        if shapes_out is not None:
            logging_fn("Output shapes: " + " ".join(f"{s}" for s in _res_shapes))

        # parse raise_if_empty
        # case: None
        if raise_if_empty is None:
            pass
        # case: "any"
        elif raise_if_empty == "any" and any(x[0] == 0 for x in _res_shapes):
            raise EmptyShapeError(
                f"At least one result from {func.__name__} is empty"  # type: ignore
            )
        # case: "all"
        elif raise_if_empty == "all" and all(x[0] == 0 for x in _res_shapes):
            raise EmptyShapeError(
                f"All results from {func.__name__} are empty"  # type: ignore
            )
        # case: something else, not in Union[Literal["any"], Literal["all"], None]
        else:
            raise TypeError("raise_if_empty must be either 'any', 'all' or None")

        return orig_res

    return wrapper


@check_parens
def timeout(
    func: Optional[Callable] = None,
    time_limit: Optional[int] = None,
    signal_handler: Optional[Callable] = None,
    signum: Union[int, Enum] = signal.SIGALRM,
) -> Callable:
    """
    Sets a time limit to a function, terminates the process if it hasn't finished within
    such time limit.

    **Warning**: This decorator uses the built-in
    [signal library](https://docs.python.org/3/library/signal.html) which fully supported
    only on UNIX.

    Arguments:
        func: function to decorate
        time_limit: max time (in seconds) for function to run, 0 means no time limit
        signal_handler: custom signal handler
        signum: signal number to be used, default=signal.SIGALRM (14), unused if custom 
            signal handler is provided

    Returns:
        decorated function

    Raises:
        ValueError: if `time_limit` is not a positive number
        TypeError: if `signum` is not an int or an Enum, or if `signal_handler` is not a \
            callable

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

    if not isinstance(time_limit, (int, float)) or time_limit <= 0:
        raise ValueError("`time_limit` should be a strictly positive number")

    if not isinstance(signum, (int, Enum)):
        raise TypeError("`signum` should be an int or an Enum")

    if signal_handler is None:

        def signal_handler(signum, frame):
            raise Exception(f"Reached time limit, terminating {func.__name__}")

        signal.signal(signum, signal_handler)  # type: ignore

    elif not callable(signal_handler):
        raise TypeError("`signal_handler` should be a callable")

    else:
        # custome signal handler provided -> bind it to the signal
        signal.signal(signum, signal_handler)

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
