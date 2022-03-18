import pytest
from deczoo import check_args


@pytest.mark.parametrize(
    "a, b, expected",
    [(1, 1, 2), (1, 2, 3)],
)
def test_check_args_no_rules(base_func, a, b, expected):
    """Tests that check_args does nothing"""
    add = check_args(base_func)

    assert add(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected, rules",
    [
        (1, 1, 2, {"a": lambda t: t > 0, "b": lambda t: t < 10}),
        (1, 2, 3, {"a": lambda t: t > 0, "b": lambda t: t < 10}),
    ],
)
def test_check_args_rules_satisfied(base_func, a, b, expected, rules):
    """Tests that check_args allows the function to run when all rules are satisfied"""
    add = check_args(base_func, **rules)

    assert add(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected, rules",
    [
        (1, 1, ValueError, {"a": lambda t: t < 0, "b": lambda t: t < 10}),
        (1, 2, ValueError, {"a": lambda t: t > 0, "b": lambda t: t > 10}),
    ],
)
def test_check_args_rules_not_satisfied(base_func, a, b, expected, rules):
    """Tests that check_args raises a ValueError if any rule is not satisfied"""
    add = check_args(base_func, **rules)

    with pytest.raises(expected):
        add(a, b)
