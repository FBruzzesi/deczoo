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

    def unlimited(x):
        for i in list(range(10**7)):
            _ = 1 + 1
        return x

    assert unlimited(x) == expected
