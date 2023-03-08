import pytest

from deczoo import retry


def test_retry_no_exceptions(base_add, capsys):
    """Tests that retry decorator works"""
    n_tries = 3
    add = retry(base_add, n_tries=n_tries, logging_fn=print)
    add(a=1, b=2)

    assert f"Attempt 1/{n_tries}: Successed" in capsys.readouterr().out


def test_retry_with_exceptions(base_add, capsys):
    """Tests that retry decorator retries when exceptions are raised"""
    n_tries = 3
    add = retry(base_add, n_tries=n_tries, logging_fn=print)
    with pytest.raises(Exception):
        add(a=1, b="a")

    sys_out = capsys.readouterr().out
    assert f"Attempt 1/{n_tries}: Failed" in sys_out
    assert f"Attempt 2/{n_tries}: Failed" in sys_out
    assert f"Attempt 3/{n_tries}: Failed" in sys_out


@pytest.mark.parametrize("n_tries", [-1, 0, 2.0, "a"])
def test_retry_invalid_n_tries(base_add, n_tries):
    """Tests that retry decorator raises ValueError when n_tries is invalid"""

    with pytest.raises(ValueError):
        retry(base_add, n_tries=n_tries)


@pytest.mark.parametrize("delay", [-1, "a"])
def test_retry_invalid_delay(base_add, delay):
    """Tests that retry decorator raises ValueError when delay is invalid"""

    with pytest.raises(ValueError):
        retry(base_add, delay=delay)
