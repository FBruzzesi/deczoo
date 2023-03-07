import pytest

from deczoo import call_counter


@pytest.mark.parametrize("seed, n_calls, expected", [(0, 5, 5), (2, 5, 7)])
def test_call_counter(base_add, seed, n_calls, expected):
    """
    Tests that call_counter keeps track of number of times function has been called,
    starting from the given seed.
    """

    add = call_counter(base_add, seed=seed)

    for _ in range(n_calls):
        add(1, 2)

    assert add._calls == expected


def test_call_counter_with_print(capsys, base_add):
    """
    Tests that call_counter logs the number of times function has been called.
    """
    add = call_counter(base_add, seed=0, log_counter=True, logging_fn=print)

    add(1, 2)
    add(1, 2)

    sys_out = capsys.readouterr().out
    assert "called 1 times" in sys_out and "called 2 times" in sys_out


def test_call_counter_raises(base_add):
    """
    Tests that call_counter raises a TypeError if seed is not an int.
    """

    with pytest.raises(TypeError):
        call_counter(base_add, seed=1.5)
