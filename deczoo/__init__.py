from importlib import metadata

from ._utils import check_parens
from .decorators import (
    call_counter,
    catch,
    check_args,
    chime_on_end,
    log,
    memory_limit,
    notify_on_end,
    retry,
    timeout,
    timer,
)

__title__ = __name__
__version__ = metadata.version(__title__)

__all__ = (
    "check_parens",
    "call_counter",
    "catch",
    "check_args",
    "chime_on_end",
    "log",
    "timer",
    "memory_limit",
    "notify_on_end",
    "retry",
    "timeout",
)
