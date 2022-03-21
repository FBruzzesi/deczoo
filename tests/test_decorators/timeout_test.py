import pytest
import time

from deczoo import timeout


def sleepy_add(a, b):
    time.sleep(2)
    return a + b


@pytest.mark.parametrize(
    "a, b, expected",
    [(1, 1, 2), (1, 2, 3)],
)
def test_within_time_limit(a, b, expected):
    """Tests that if the function runs within time limit returns true value"""
    add = timeout(sleepy_add, time_limit=3)

    assert add(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [(1, 1, Exception), (1, 2, Exception)],
)
def test_within_time_limit(a, b, expected):
    """Tests that if the function doesn't make it in time, an Exception is raised"""
    add = timeout(sleepy_add, time_limit=1)

    with pytest.raises(expected):
        add(a, b)
