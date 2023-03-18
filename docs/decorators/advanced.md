# Advanced Usage

## Wraps

[`functools.wraps`](https://docs.python.org/3/library/functools.html#functools.wraps) is a utility function in the Python standard library that is often used in decorators to preserve the original function's metadata (such as its name, docstring, and annotations) in the wrapper function.

Here's an example of how `functools.wraps` can be used in a decorator, and how the metadata's differ:

=== "with \@wraps"

    ```python hl_lines="1 4 18 19"
    from functools import wraps

    def dec_with_wraps(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Do something before the function is called
            result = func(*args, **kwargs)
            # Do something after the function is called
            return result
        return wrapper

    @dec_with_wraps
    def my_func():
        """This is my function"""
        return "Hello, world!"

    print(f"Name = '{my_func.__name__}'", f"Docs = '{my_func.__doc__}'", sep="\n")
    # Name = 'my_func'
    # Docs = 'This is my function'
    ```

=== "without \@wraps"

    ```python hl_lines="15 16"
    def dec_no_wraps(func):
        def wrapper(*args, **kwargs):
            # Do something before the function is called
            result = func(*args, **kwargs)
            # Do something after the function is called
            return result
        return wrapper

    @dec_no_wraps
    def my_func():
        """This is my function"""
        return "Hello, world!"

    print(f"Name = '{my_func.__name__}'", f"Docs = '{my_func.__doc__}'", sep="\n")
    # Name = 'wrapper'
    # Docs = 'None'
    ```

As you can see, the two decorators `dec_with_wraps` and `dec_no_wraps` are indentical; the only difference between the two cases is the use of `@wraps` decorator in the former to preserve the metadata of the original function.

When we print the `__name__` and `__doc__` attributes of the function in the two different scenarios, we obtain completely different results! In particular, in the first case the metadata of the decorated `my_func` are maintained, in the latter the metadata we obtain are those of the `wrapper` function inside the decorator.

## Decorators with arguments

<img src="../img/deeper-meme.jpg" width=230 height=230 align="right">

Sometimes we have more complexity to model and to achieve that we need to be able to pass arguments to our decorator.

Let's assume that we want to run a function twice, or 3-times, or 4-times and so on.

Instead of writing differnt decorators that run the input function N times, we can go one level deeper, and define a function that takes the decorator arguments and returns the actual decorator function.

```python
from functools import wraps
from typing import Callable

def repeat_n_times(n: int) -> Callable:
    """Gets as input the arguments to be used in the actual decorator"""

    def decorator(func: Callable) -> Callable:
        """This is the actual decorator!"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            """Returns a list with N func results"""
            return [func(*args, **kwargs) for _ in range(n)]

        return wrapper

    return decorator

@repeat_n_times(n=3)
def say_hello(name: str) -> str:
    return f"Hello, {name}!"

print(say_hello("Francesco"))
# ['Hello, Francesco!', 'Hello, Francesco!', 'Hello, Francesco!']
```

<img src="../img/confused.gif" width=230 height=230 align="right">

Do you feel confused? If the answer is yes, it is because it is kinda confusing!

A decorator with arguments is a function that takes arguments and returns another function that acts as the *actual* decorator.

This decorator function takes a function as an argument and returns a new function that modifies the original function in some way.

The key difference between a decorator with arguments and a regular decorator is that the decorator with arguments has an extra layer of nested functions. The outer function takes the arguments and returns the actual decorator function, while the inner function takes the original function as an argument and returns the modified function.

Can we do it differently??? Sure we can, and that's how all decorators in **deczoo** are implemented.

## Decorators with arguments, pt.2
