from typing import Callable

try:
    from rich.console import Console
    from rich.theme import Theme

    custom_theme = Theme({"good": "bold green", "bad": "bold red"})
    console = Console(theme=custom_theme)

    LOGGING_FN = console.print

except:
    LOGGING_FN = print


'''
def set_logging_fn(func: Callable = None):
    """
    Set the current logging_fn.

    Argument:
        func: The change will be switched if a valid name is provided. The current theme is
            returned if `None`.
    Raises:
        ValueError: If the theme is unknown.
    """

    global LOGGING_FN

    if func is None:
        return LOGGING_FN
    elif not isinstance(func, Callable):
        raise ValueError("func is not callable, please provide a callable logging function")
    else:
        LOGGING_FN = func
'''
