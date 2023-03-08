import pytest

from deczoo import log


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
