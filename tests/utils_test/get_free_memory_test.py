import os

import pytest

from deczoo._utils import _get_free_memory


@pytest.mark.skipif(os.name != "posix", reason="This test runs only on Unix-based systems")
def test_get_free_memory():
    """
    Tests _get_free_memory function

    The @pytest.mark.skipif(...) decorator skips the test if the operating system is not
    a Unix-based system.
    """
    assert isinstance(_get_free_memory(), int)
    assert _get_free_memory() >= 0
