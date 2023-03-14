from typing import Tuple

import pytest

from deczoo._utils import HasShape


class TestShape:
    """Test class for HasShape with shape attribute"""

    @property
    def shape(self) -> Tuple[int, ...]:

        return (1, 2)


class NoShape:
    """Test class for HasShape without shape attribute"""

    pass


def test_protocol():
    """Tests that HasShape is protocol and cannot be instantiated"""
    with pytest.raises(TypeError):
        HasShape()


def test_protocol_implemented():
    """Tests that TestShape is a valid implementation of HasShape"""
    assert isinstance(TestShape, HasShape)
    assert hasattr(TestShape, "shape")


def test_protocol_not_implemented():
    """Tests that NoShape is not a valid implementation of HasShape"""

    assert not isinstance(NoShape, HasShape)
    assert not hasattr(NoShape, "shape")
