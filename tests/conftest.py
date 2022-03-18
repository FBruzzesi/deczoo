import pytest


@pytest.fixture(scope="module")
def base_func():
    """Fixture for base function to decorate"""

    def _add(a, b):
        """Adding a and b"""
        return a + b

    return _add
