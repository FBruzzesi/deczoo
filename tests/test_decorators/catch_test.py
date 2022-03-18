import pytest
from deczoo import catch


@pytest.mark.parametrize(
    "a, b, return_on_exception, expected",
    [(1, 2, -999, 3), (1, "a", -999, -999), (1, "a", 0, 0)],
)
def test_catch_return_on_exception(base_func, a, b, return_on_exception, expected):
    """Tests that catch returns return_on_exception value"""
    add = catch(base_func, return_on_exception=return_on_exception)

    assert add(a, b) == expected


@pytest.mark.parametrize(
    "a, b, raise_on_execption, expected",
    [
        (1, "a", ValueError, ValueError),
        (1, "a", Exception, Exception),
        (1, "a", None, Exception),
    ],
)
def test_catch_raise_on_exception(base_func, a, b, raise_on_execption, expected):
    """Tests that catch raises the raise_on_execption exception"""
    add = catch(base_func, raise_on_execption=raise_on_execption)

    with pytest.raises(expected):
        add(a, b)
