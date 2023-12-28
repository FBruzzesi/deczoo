from contextlib import nullcontext as does_not_raise

import pytest

from deczoo import catch


@pytest.mark.parametrize(
    "value, context",
    [
        (1.1, pytest.raises(TypeError)),
        ("a", pytest.raises(TypeError)),
        ((1, 2), pytest.raises(TypeError)),
        (print, does_not_raise()),
    ],
)
def test_params(base_add, value, context):
    """
    Tests that catch parse its params.
    """

    with context:
        catch(base_add, logging_fn=value)


@pytest.mark.parametrize(
    "b, return_on_exception, expected",
    [(2, -999, 3), ("a", -999, -999), ("a", 0, 0)],
)
def test_return(base_add, b, return_on_exception, expected):
    """Tests that catch returns return_on_exception value"""
    add = catch(base_add, return_on_exception=return_on_exception)

    assert add(a=1, b=b) == expected


@pytest.mark.parametrize(
    "raise_on_exception, context",
    [
        (ValueError, pytest.raises(ValueError)),
        (Exception, pytest.raises(Exception)),
        (None, pytest.raises(Exception)),
    ],
)
def test_raise(base_add, raise_on_exception, context):
    """Tests that catch raises the raise_on_exception exception"""
    add = catch(base_add, raise_on_exception=raise_on_exception)

    with context:
        add(a=1, b="a")
