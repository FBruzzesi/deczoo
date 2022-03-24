import pytest
from deczoo import call_counter


@pytest.mark.parametrize("seed, n_calls, expected", [(0, 5, 5), (2, 5, 7)])
def test_call_counter(base_add, seed, n_calls, expected):
    """Tests that call_counter keeps track of number of times function has been called"""

    add = call_counter(base_add, seed=seed)

    for _ in range(n_calls):
        add(1, 2)

    assert add._calls == expected
