from contextlib import nullcontext as does_not_raise

import pytest

from deczoo import call_counter


@pytest.mark.parametrize("arg_name", ["seed", "log_counter", "logging_fn"])
@pytest.mark.parametrize("value", [1.1, "a", (1, 2)])
def test_params_raise(base_add, arg_name, value):
    """
    Tests that call_counter raises an error if invalid parameter is passed.
    """

    with pytest.raises(TypeError):
        call_counter(base_add, **{arg_name: value})


@pytest.mark.parametrize(
    "arg_name, value",
    [("seed", 1), ("log_counter", True), ("log_counter", False), ("logging_fn", print)],
)
def test_params_valid(base_add, arg_name, value):
    """
    Tests that call_counter doesn't raise an error if valid parameter type is passed.
    """

    with does_not_raise():
        call_counter(base_add, **{arg_name: value})


@pytest.mark.parametrize("seed", list(range(-10, 10, 2)))
@pytest.mark.parametrize("n_calls", list(range(1, 5)))
def test_counting(base_add, seed, n_calls):
    """
    Tests that call_counter keeps track of number of times function has been called,
    starting from the given seed.
    """
    expected = seed + n_calls
    add = call_counter(base_add, seed=seed)

    for _ in range(n_calls):
        add(1, 2)

    assert add._calls == expected


@pytest.mark.parametrize("n_calls", list(range(1, 5)))
def test_sys(capsys, base_add, n_calls):
    """
    Tests that call_counter logs the number of times function has been called.
    """
    add = call_counter(base_add, seed=0, log_counter=True, logging_fn=print)

    for _ in range(n_calls):
        add(1, 2)

    sys_out = capsys.readouterr().out
    assert all(f"called {x} times" in sys_out for x in range(1, n_calls + 1))
