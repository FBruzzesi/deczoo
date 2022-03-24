import pytest
import time


@pytest.fixture(scope="module")
def base_add():
    """Fixture for base function to decorate"""

    def _add(a, b):
        """Adding a and b"""
        return a + b

    return _add


@pytest.fixture(scope="module")
def sleepy_add():
    """Fixture for base function to decorate"""

    def _add(a, b):
        """Adds a and b after sleeping for 2 seconds"""
        time.sleep(2)
        return a + b

    return _add
