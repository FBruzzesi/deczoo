import sys
from abc import ABCMeta, abstractmethod

if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

PS = ParamSpec("PS")


class BaseNotifier(metaclass=ABCMeta):
    """Abstract base class to create a notifier to use in `notify_on_end` decorator.

    The class should have a `.notify()` method which gets called after the decorated function has finished running.
    """

    @abstractmethod
    def notify(self: Self, *args: PS.args, **kwargs: PS.kwargs) -> None:
        """Method used to notify"""
        ...
