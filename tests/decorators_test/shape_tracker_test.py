from contextlib import nullcontext as does_not_raise

import numpy as np
import pytest

from deczoo import shape_tracker
from deczoo._utils import EmptyShapeError


@pytest.mark.parametrize(
    "arg_name, value, context",
    [
        ("shape_in", True, does_not_raise()),
        ("shape_out", True, does_not_raise()),
        ("shape_delta", True, does_not_raise()),
        ("raise_if_empty", True, does_not_raise()),
        ("shape_in", False, does_not_raise()),
        ("shape_out", False, does_not_raise()),
        ("shape_delta", False, does_not_raise()),
        ("raise_if_empty", False, does_not_raise()),
        ("arg_to_track", 0, does_not_raise()),
        ("arg_to_track", "a", does_not_raise()),
        ("logging_fn", print, does_not_raise()),
        ("shape_in", 42, pytest.raises(TypeError)),
        ("shape_out", 1.0, pytest.raises(TypeError)),
        ("shape_delta", "a", pytest.raises(TypeError)),
        ("raise_if_empty", {1: 2}, pytest.raises(TypeError)),
        ("arg_to_track", (1, 2), pytest.raises(TypeError)),
        ("logging_fn", [1, 2], pytest.raises(TypeError)),
    ],
)
def test_params(base_add, arg_name, value, context):
    """Tests that shape_tracker raises TypeError when invalid params are passed"""
    with context:
        shape_tracker(base_add, **{arg_name: value})


# Since we tested for param errors, now we can just test for every boolean turned on
@pytest.mark.parametrize(
    "arg_to_track, n, context",
    [
        (0, 3, does_not_raise()),
        ("a", 3, does_not_raise()),
        (0, 0, pytest.raises(EmptyShapeError)),
        ("a", 0, pytest.raises(EmptyShapeError)),
        (1, 3, pytest.raises(AttributeError)),
        ("b", 3, pytest.raises(KeyError)),
    ],
)
def test_shape_in(capsys, arg_to_track, n, context):
    """Tests that shape_tracker tracks input shape"""
    a_shape = (1, 2)

    @shape_tracker(
        shape_in=True,
        shape_out=True,
        shape_delta=True,
        raise_if_empty=True,
        arg_to_track=arg_to_track,
        logging_fn=print,
    )
    def n_vstack(a: np.ndarray, n: int) -> np.ndarray:
        if n > 0:
            return np.vstack(n * [a])
        else:
            return np.empty(0)

    with context:
        n_vstack(np.ones(a_shape), n)
        sys_out = capsys.readouterr().out

        assert "Input: `a` has shape" in sys_out
        assert "Output: result has shape " in sys_out
        assert "Shape delta: " in sys_out
