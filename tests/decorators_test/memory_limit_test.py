from contextlib import nullcontext as does_not_raise

import pytest

from deczoo import memory_limit


@pytest.mark.parametrize(
    "arg_name, value, context",
    [
        ("percentage", 2, pytest.raises(TypeError)),
        ("percentage", "a", pytest.raises(TypeError)),
        ("percentage", (1, 2), pytest.raises(TypeError)),
        ("logging_fn", 2, pytest.raises(TypeError)),
        ("logging_fn", "a", pytest.raises(TypeError)),
        ("logging_fn", (1, 2), pytest.raises(TypeError)),
        ("percentage", 2.0, pytest.raises(ValueError)),
        ("percentage", -1.0, pytest.raises(ValueError)),
        ("percentage", 0.0, does_not_raise()),
        ("percentage", 0.5, does_not_raise()),
        ("percentage", 1.0, does_not_raise()),
        ("logging_fn", print, does_not_raise()),
    ],
)
def test_params(base_add, arg_name, value, context):
    """
    Tests that memory_limit raises an error if invalid parameter is passed.
    """

    with context:
        memory_limit(base_add, **{arg_name: value})


@pytest.mark.parametrize(
    "percentage, context",
    [
        (0.01, pytest.raises(MemoryError)),
        (0.02, pytest.raises(MemoryError)),
        (0.95, does_not_raise()),
        (1.0, does_not_raise()),
    ],
)
def test_memory_limit(capsys, percentage, context):
    """Tests that memory limited function raises MemoryError exception"""

    @memory_limit(percentage=percentage, logging_fn=print)
    def limited(x):
        for i in list(range(10**7)):
            _ = 1 + 1
        return x

    with context:
        limited(42)

        sys_out = capsys.readouterr().out
        assert f"Setting memory limit for {limited.__name__} to" in sys_out
