import pytest

from deczoo import shape_tracker

# TODO: Add tests for shape_tracker


@pytest.mark.parametrize(
    "kwarg, value",
    [
        ("shape_in", 42),
        ("shape_out", "a"),
        ("shape_delta", (1, 2)),
        ("raise_if_empty", 1.1),
        ("arg_to_track", -1),
        ("arg_to_track", 1.1),
        ("arg_to_track", (1, 2)),
    ],
)
def test_shape_input_validation(base_add, kwarg, value):
    """Tests that shape_tracker raises TypeError when invalid kwargs are passed"""
    with pytest.raises(TypeError):
        shape_tracker(base_add, **{kwarg: value})
