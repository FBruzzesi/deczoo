import abc


class BaseNotifier(metaclass=abc.ABCMeta):
    """
    Base class to create a notifier to use in `notify_on_end` decorator.
    The class should have a `notify` method which is called after the decorated function
    has finished running.
    """

    @abc.abstractmethod
    def notify(self, *args, **kwargs):
        """Method used to notify"""
        pass
