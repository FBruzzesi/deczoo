from contextlib import nullcontext as does_not_raise

import pytest

from deczoo import check_args


@pytest.mark.parametrize(
    "rules, context",
    [
        ({"a": lambda t: t > 0, "b": lambda t: t < 10}, does_not_raise()),
        ({}, does_not_raise()),
        ({"a": True}, pytest.raises(ValueError)),
        ({"a": lambda t: t > 0, "b": "test"}, pytest.raises(ValueError)),
    ],
)
def test_params(base_add, rules, context):
    """
    Tests that check_args raises an error if invalid parameter is passed.
    """

    with context:
        check_args(base_add, **rules)


@pytest.mark.parametrize(
    "rules, context",
    [
        ({"a": lambda t: t > 0, "b": lambda t: t > 0}, does_not_raise()),
        ({"a": lambda t: t < 2, "b": lambda t: t > 0}, does_not_raise()),
        ({"a": lambda t: t > 0, "b": lambda t: t < 0}, pytest.raises(ValueError)),
        ({"a": lambda t: t < 0, "b": lambda t: t > 0}, pytest.raises(ValueError)),
    ],
)
def test_rules(base_add, rules, context):
    """
    Tests that check_args applies the rules correctly.
    """
    add = check_args(base_add, **rules)

    with context:
        add(a=1, b=1)
