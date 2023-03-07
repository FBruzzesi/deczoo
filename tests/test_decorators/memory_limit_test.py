import pytest

from deczoo import memory_limit


@pytest.mark.parametrize(
    "x, expected",
    [("hello world", MemoryError)],
)
def test_limited(x, expected):
    """Tests that memory limited function raises MemoryError exception"""

    @memory_limit(percentage=0.05)
    def limited(x):

        for i in list(range(10**7)):
            _ = 1 + 1
        return x

    with pytest.raises(expected):
        limited(x)


@pytest.mark.parametrize(
    "x, expected",
    [("hello world", "hello world"), (42, 42)],
)
def test_unlimited(x, expected):
    """Tests that without limiting memory the test passes"""

    @memory_limit(percentage=1.0)
    def unlimited(x):
        for i in list(range(10**7)):
            _ = 1 + 1
        return x

    assert unlimited(x) == expected


@pytest.mark.parametrize(
    "p, expected",
    [("a", TypeError), ("0.99", TypeError), (-1.0, ValueError), (1.1, ValueError)],
)
def test_invalid_percentage(base_add, p, expected):
    """Tests that memory_limit raises TypeError if percentage is not a float"""

    with pytest.raises(expected):
        memory_limit(base_add, percentage=p)
