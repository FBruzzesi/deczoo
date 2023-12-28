from contextlib import nullcontext as does_not_raise
from typing import Tuple

import numpy as np
import pytest

from deczoo import multi_shape_tracker
from deczoo._utils import EmptyShapeError

a = np.ones((1, 2))
b = np.ones((1, 2))


def add_multi(a: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Function to test multi_shape_tracker"""
    return a + b, a * b


@pytest.mark.parametrize("arg_name", ["shapes_in", "shapes_out", "raise_if_empty", "logging_fn"])
@pytest.mark.parametrize("value", [1.1, {1: 2}, ("a", 1), (0, "b"), "a"])
def test_invalid_args(arg_name, value):
    """Tests that multi_shape_tracker raises a TyperError any invalid args are passed"""
    if arg_name == "shapes_in" and value == "a":
        pytest.skip("Not of interest")

    with pytest.raises(TypeError):
        _ = multi_shape_tracker(add_multi, **{arg_name: value})(a, b)


@pytest.mark.parametrize("value", ["a", "b", ("a", "b"), 0, 1, (0, 1), None])
def test_valid_shapes_in(capsys, value):
    """Tests that multi_shape_tracker doesn't raise an error for valid shapes_in param"""

    with does_not_raise():
        _ = multi_shape_tracker(add_multi, shapes_in=value)(a, b)

        if value is not None:
            sys_out = capsys.readouterr().out
            assert "Input shapes: " in sys_out


@pytest.mark.parametrize("value", ["all", 0, 1, (0, 1), None])
def test_valid_shapes_out(capsys, value):
    """Tests that multi_shape_tracker doesn't raise an error for valid shapes_out param"""

    with does_not_raise():
        _ = multi_shape_tracker(add_multi, shapes_out=value)(a, b)

        if value is not None:
            sys_out = capsys.readouterr().out
            assert "Output shapes: " in sys_out


@pytest.mark.parametrize("value", ["all", "any", None])
@pytest.mark.parametrize(
    "shapes, context",
    [((1, 2), does_not_raise()), ((0,), pytest.raises(EmptyShapeError))],
)
def test_valid_raise_if_empty(value, shapes, context):
    """Tests that multi_shape_tracker doesn't raise an error for valid raise_if_empty"""

    a = np.ones(shapes)
    b = np.ones(shapes)

    # forcing to switch context if value is None
    context = context if value is not None else does_not_raise()

    with context:
        _ = multi_shape_tracker(add_multi, raise_if_empty=value)(a, b)


def test_valid_logging_fn():
    """Tests that multi_shape_tracker doesn't raise an error for valid logging_fn param"""

    with does_not_raise():
        _ = multi_shape_tracker(add_multi, logging_fn=print)(a, b)


# multi_shape_tracker(
#     func: Optional[Callable[[HasShape, Sequence[Any]], Tuple[HasShape, ...]]] = None,
#     shapes_in: Optional[Union[str, int, Sequence[str], Sequence[int]]] = None,
#     shapes_out: Optional[Union[int, Sequence[int], Literal["all"]]] = "all",
#     raise_if_empty: Optional[Literal["any", "all"]] = "any",
#     logging_fn: Callable = LOGGING_FN,
# ) -> Callable:
