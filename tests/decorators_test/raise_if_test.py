from contextlib import nullcontext as does_not_raise

import pytest

from deczoo import raise_if


@pytest.mark.parametrize(
    "condition, context",
    [
        (lambda: True, pytest.raises(ValueError)),
        (lambda: False, does_not_raise()),
    ],
)
def raise_if_test(condition, context):
    """Test raise_if decorator."""
    err_msg = "Test exception"

    @raise_if(condition, exception=ValueError, message=err_msg)
    def dummy_function():
        pass

    with context as exc_info:
        dummy_function()

    if exc_info:
        assert err_msg in str(exc_info.value)
