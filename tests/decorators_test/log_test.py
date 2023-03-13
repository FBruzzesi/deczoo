from contextlib import nullcontext as does_not_raise

import pytest

from deczoo import log


@pytest.mark.parametrize(
    "arg_name, value, context",
    [
        ("log_time", 1.1, pytest.raises(TypeError)),
        ("log_args", "a", pytest.raises(TypeError)),
        ("log_error", (1, 2), pytest.raises(TypeError)),
        ("log_file", 1.1, pytest.raises(TypeError)),
        ("logging_fn", {}, pytest.raises(TypeError)),
        ("log_time", True, does_not_raise()),
        ("log_args", False, does_not_raise()),
        ("log_error", False, does_not_raise()),
        ("log_file", "test.txt", does_not_raise()),
        ("logging_fn", print, does_not_raise()),
    ],
)
def test_params(base_add, arg_name, value, context):
    """Tests that log raises an error if invalid parameter is passed."""

    with context:
        log(base_add, **{arg_name: value})


@pytest.mark.parametrize(
    "log_time, log_args, expected",
    [
        (True, False, "add time="),
        (False, True, "add args=(a=1, b=2)"),
        (True, True, "add args=(a=1, b=2) time="),
    ],
)
def test_log_no_exceptions(base_add, capsys, log_time, log_args, expected):
    """Tests that log decorator works"""

    add = log(
        base_add,
        log_time=log_time,
        log_args=log_args,
        logging_fn=print,
    )

    add(a=1, b=2)

    sys_out = capsys.readouterr().out
    assert expected in sys_out


def test_log_with_exceptions(base_add, capsys):
    """Tests that log decorator logs exceptions"""

    add = log(base_add, log_time=False, log_args=False, log_error=True, logging_fn=print)

    with pytest.raises(Exception):
        add(a=1, b="a")

    sys_out = capsys.readouterr().out
    assert "add Failed with error: " in sys_out


def test_log_file(base_add, tmp_path):
    """Tests that log decorator logs to file"""

    log_file = tmp_path / "log.txt"

    add = log(
        base_add,
        log_time=False,
        log_args=True,
        log_file=log_file,
        logging_fn=print,
    )

    add(a=1, b=2)
    with open(log_file) as f:
        assert "add args=(a=1, b=2)" in f.read()
