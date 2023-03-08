import pytest

from deczoo._base_notifier import BaseNotifier


def test_base_notifier():
    """Tests that BaseNotifier is abstract"""
    with pytest.raises(TypeError):
        BaseNotifier()

    class TestNotifier(BaseNotifier):
        """Concrete implementation of BaseNotifier"""

        def notify(self, *args, **kwargs) -> None:
            """Method used to notify"""
            print("Notified")

    assert TestNotifier()
    assert TestNotifier().notify() is None
