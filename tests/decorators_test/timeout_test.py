from contextlib import nullcontext as does_not_raise

import pytest

from deczoo import timeout


@pytest.mark.parametrize(
    "arg_name, value, context",
    [
        ("time_limit", -1, pytest.raises(ValueError)),
        ("time_limit", 1.0, pytest.raises(ValueError)),
        ("time_limit", "a", pytest.raises(ValueError)),
        ("time_limit", (1, 2), pytest.raises(ValueError)),
        ("signum", "a", pytest.raises(TypeError)),
        ("signum", (1, 2), pytest.raises(TypeError)),
        ("signal_handler", "a", pytest.raises(TypeError)),
        ("signal_handler", (1, 2), pytest.raises(TypeError)),
        ("time_limit", 1, does_not_raise()),
        ("signum", 1, does_not_raise()),
        ("signal_handler", lambda x, y: (x, y), does_not_raise()),
    ],
)
def test_params(base_add, arg_name, value, context):
    """
    Tests that timeout raises an error if invalid parameter is passed.
    """

    with context:
        if arg_name != "time_limit":
            timeout(base_add, time_limit=1, **{arg_name: value})
        else:
            timeout(base_add, **{arg_name: value})


@pytest.mark.parametrize(
    "b, time_limit, context",
    [
        (1, 1, pytest.raises(TimeoutError)),
        (1, 2, pytest.raises(TimeoutError)),
        (
            "a",
            1,
            pytest.raises(TimeoutError),
        ),  # TimeoutError is raised before TypeError
        (1, 3, does_not_raise()),
        ("a", 3, pytest.raises(TypeError)),
    ],
)
def test_out_of_limit(sleepy_add, b, time_limit, context):
    """Tests that if the function doesn't make it in time TimeoutError is raised"""

    with context:
        _ = timeout(sleepy_add, time_limit=time_limit)(1, b=b)
