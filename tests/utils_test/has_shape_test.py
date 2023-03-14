from typing import Tuple

import pytest

from deczoo._utils import HasShape


class TestShape:
    """Test class for HasShape"""

    @property
    def shape(self) -> Tuple[int, ...]:

        return (1, 2)


def test_has_shape():
    """Tests that HasShape is protocol"""
    with pytest.raises(TypeError):
        HasShape()


def test_protocol():
    """Tests that TestShape is a valid implementation of HasShape"""
    assert isinstance(TestShape, HasShape)
