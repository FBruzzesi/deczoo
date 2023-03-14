from contextlib import nullcontext as does_not_raise

import pytest

from deczoo import notify_on_end
from deczoo._base_notifier import BaseNotifier


class TestNotifier(BaseNotifier):
    """
    Test notifier class, concrete implementation of BaseNotifier used for testing
    """

    def notify(self, *args, **kwargs):
        """Method used to notify"""
        print("Notified")


class TestNotNotifier:
    """Test class that is not a notifier"""

    def notify(self, *args, **kwargs):
        """Method used to notify"""
        ...


@pytest.mark.parametrize(
    "notifier, context",
    [(TestNotifier(), does_not_raise()), (TestNotNotifier(), pytest.raises(TypeError))],
)
def test_params(base_add, notifier, context):
    """Tests that notify_on_end raises an error if invalid parameter is passed."""

    with context:
        notify_on_end(base_add, notifier=notifier)


@pytest.mark.parametrize(
    "a, b, exception",
    [(1, 2, does_not_raise()), (1, "a", pytest.raises(Exception))],
)
def test_notify(base_add, capsys, a, b, exception):
    """Tests that notify method get called"""

    add = notify_on_end(base_add, notifier=TestNotifier())

    with exception:
        add(a=a, b=b)

        sys_out = capsys.readouterr().out
        assert "Notified" in sys_out
