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


@pytest.mark.parametrize(
    "a, b, exception",
    [(1, 2, does_not_raise()), (1, "a", pytest.raises(Exception))],
)
def test_notify_on_end(base_add, capsys, a, b, exception):
    """Tests that notify_on_end decorator works"""

    add = notify_on_end(base_add, notifier=TestNotifier())

    with exception:
        add(a=a, b=b)

        sys_out = capsys.readouterr().out
        assert "Notified" in sys_out
