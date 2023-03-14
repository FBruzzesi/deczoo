import pytest

from deczoo._utils import EmptyShapeError


def test_empty_shape_error():
    """Test EmptyShapeError class"""

    msg = "Test message"
    with pytest.raises(EmptyShapeError) as excinfo:
        raise EmptyShapeError(msg)

    assert str(excinfo.value) == msg
