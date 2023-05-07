from unittest.mock import patch

import pytest

from deczoo import chime_on_end


def test_success(base_add):
    """Tests that chime.success is called when function finishes successfully."""

    with patch("chime.success") as mock_success:
        _ = chime_on_end(base_add)(1, 2)
        mock_success.assert_called_once()


def test_error():
    """Tests that chime.error is called when function raises an error."""

    with patch("chime.error") as mock_error:

        @chime_on_end
        def mock_func(x):
            raise ValueError("Something went wrong")

        with pytest.raises(ValueError):
            mock_func(10)

        mock_error.assert_called_once
