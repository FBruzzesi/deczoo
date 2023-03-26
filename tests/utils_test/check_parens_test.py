from deczoo._utils import check_parens


def test_check_parens(capsys):
    """
    Tests that once a decorator is itself decorated with check_parens, it can be
    called with or without parens.
    """

    @check_parens
    def decorator(func, arg1="default1", arg2="default2"):
        def wrapper(*args, **kwargs):
            print(arg1, arg2)
            return func(*args, **kwargs)

        return wrapper

    @decorator
    def _with_default():
        return "default"

    @decorator(arg1="custom1", arg2="custom2")
    def _with_custom():
        return "custom"

    assert _with_default() == "default"
    assert _with_custom() == "custom"

    all_args = ("default1", "default2", "custom1", "custom2")
    sys_out = capsys.readouterr().out

    assert all(a in sys_out for a in all_args)
