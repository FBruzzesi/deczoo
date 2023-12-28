from contextlib import nullcontext as does_not_raise

import pytest

from deczoo import retry


@pytest.mark.parametrize(
    "arg_name, value, context",
    [
        ("n_tries", 0, pytest.raises(ValueError)),
        ("n_tries", 0.5, pytest.raises(ValueError)),
        ("delay", "a", pytest.raises(ValueError)),
        ("delay", -2, pytest.raises(ValueError)),
        ("logging_fn", "a", pytest.raises(TypeError)),
        ("logging_fn", (1, 2), pytest.raises(TypeError)),
        ("n_tries", 1, does_not_raise()),
        ("n_tries", 2, does_not_raise()),
        ("delay", 1, does_not_raise()),
        ("delay", 1.0, does_not_raise()),
        ("logging_fn", print, does_not_raise()),
    ],
)
def test_params(base_add, arg_name, value, context):
    """
    Tests that retry raises an error if invalid parameter is passed.
    """

    with context:
        retry(base_add, **{arg_name: value})


@pytest.mark.parametrize("n_tries", list(range(2, 5)))
@pytest.mark.parametrize("delay", [0.0, 0.1])
def test_retry_no_exceptions(base_add, capsys, n_tries, delay):
    """Tests that retry decorator works"""
    _ = retry(base_add, n_tries=n_tries, delay=delay, logging_fn=print)(a=1, b=2)
    assert f"Attempt 1/{n_tries}: Succeeded" in capsys.readouterr().out


@pytest.mark.parametrize("n_tries", list(range(2, 5)))
@pytest.mark.parametrize("delay", [0.0, 0.1])
def test_retry_with_exceptions(base_add, capsys, n_tries, delay):
    """Tests that retry decorator retries when exceptions are raised"""
    add = retry(base_add, n_tries=n_tries, delay=delay, logging_fn=print)
    with pytest.raises(Exception):
        add(a=1, b="a")

    sys_out = capsys.readouterr().out
    assert all(f"Attempt {x}/{n_tries}: Failed" in sys_out for x in range(1, n_tries + 1))
