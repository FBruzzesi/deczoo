# Introduction

## What is a decorator?

In Python, a decorator is a way to modify or enhance the behavior of a function or a class without actually modifying the source code of the function or class.

Defining this _additional behaviour_ in a decorator, instead of within the original function itself, allows us to re-use it every time we need it, without a tedious _copy-pasting_.

Decorators are implemented as functions (or classes) that take a function or a class as input and return a new function or class that has some additional functionality.

Here is a simple example in order to illustrate the concept:

```python
from typing import Callable

def my_decorator(func: Callable) -> Callable:
    """
    - `func` is the function taken as input to our decorator
    - `func` behaviour will be modified/enhanced
    - `wrapper` is the function that the decorator returns
    """

    def wrapper(*args, **kwargs):

        print(f"Starting to run {func.__name__}")
        res = func(*args, **kwargs)
        print(f"{func.__name__} finished running!")

        return res

    return wrapper
```

Here, `my_decorator` is a function that takes a function as input, denoted as `func`, and returns a new function called `wrapper` defined within the inner scope. In this case, `wrapper` contains some additional functionalities (in this case, the `print` statements) that are executed before and after the original function call.

`wrapper` function takes any number of positional and keyword arguments (`*args` and `**kwargs`), calls the original function `func` with those arguments, and returns the original result of the function call `res`.

## Decorator syntax

We just saw what is a decorator and how to code one, but how can we use it?

There are two equivalent options available:

- _Functional assignment_, we assign the output of the decorator to a new function:

    ```python
    def my_func():
        print("Hello world!")
        return 42

    my_func = my_decorator(my_func)
    ```

- The (more pythonic) _`@`-syntax_ (also called _decorator syntax_ or _decorator notation_), this is a shorthand way of applying a decorator to a function or a class, without having to explicitly call the decorator function and passing the function or class as an argument:

    ```python
    @my_decorator
    def my_func():
        print("Hello world!")
        return 42
    ```

In both cases, calling the function results in the following:

```python
result = my_func()
# Starting to run my_func
# Hello world!
# my_func finished running!

result
# 42
```
