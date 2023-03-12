import pytest

from deczoo import shape_tracker


@pytest.mark.parametrize(
    "kwarg, value",
    [
        ("shape_in", 42),
        ("shape_out", "a"),
        ("shape_delta", (1, 2)),
        ("raise_if_empty", 1.1),
        ("idx_to_track", "a"),
        ("idx_to_track", -1),
    ],
)
def test_shape_input_validation(base_add, kwarg, value):
    """Tests that shape_tracker raises TypeError when invalid kwargs are passed"""
    with pytest.raises(TypeError):
        shape_tracker(base_add, **{kwarg: value})
