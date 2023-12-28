# Advanced Usage

## Stacks

We're not limited to a single decorator per function, we can _stack_ how many we want.

Let's see how that works:

```python
def decorator1(func):
    def wrapper(*args, **kwargs):

        print("Decorator 1")
        return func(*args, **kwargs)

    return wrapper

def decorator2(func):
    def wrapper(*args, **kwargs):

        print("Decorator 2")
        return func(*args, **kwargs)

    return wrapper
```

Remark that the _order_ in which we stack decorators matter:

=== "\@d1 \@d2"

    ```python hl_lines="1 2 8 9"

    @decorator1
    @decorator2
    def func():
        print("Hello world!")
        return 42

    func()
    # Decorator 1
    # Decorator 2
    # Hello world!
    ```

=== "\@d2 \@d1"

    ```python hl_lines="1 2 8 9"

    @decorator2
    @decorator1
    def func():
        print("Hello world!")
        return 42

    func()
    # Decorator 2
    # Decorator 1
    # Hello world!
    ```

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

As you can see, the two decorators `dec_with_wraps` and `dec_no_wraps` are identical; the only difference between the two cases is the use of `@wraps` decorator in the former to preserve the metadata of the original function.

When we print the `__name__` and `__doc__` attributes of the function in the two different scenarios, we obtain completely different results! In particular, in the first case the metadata of the decorated `my_func` are maintained, in the latter the metadata we obtain are those of the `wrapper` function inside the decorator.

## Decorators with arguments

<img src="../../img/deeper-meme.jpg" width=230 height=230 align="right">

Sometimes we have more complexity to model and to achieve that we need to be able to pass arguments to our decorator.

Let's assume that we want to run a function twice, or 3-times, or 4-times and so on.

Instead of writing different decorators that run the input function N times, we can go one level deeper, and define a function that takes the decorator arguments and returns the actual decorator function.

```python title="repeat_n_times"
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

@repeat_n_times(n=2)
def say_hello(name: str) -> str:
    return f"Hello {name}!"

print(say_hello("Fra"))
# ['Hello Fra!', 'Hello Fra!']
```

<img src="../../img/confused.gif" width=230 height=230 align="right">

Do you feel confused? If the answer is yes, it is because it is kinda confusing!

A decorator with arguments is a function that takes arguments and returns another function that acts as the *actual* decorator.

This decorator function takes a function as an argument and returns a new function that modifies the original function in some way.

The key difference between a decorator with arguments and a regular decorator is that the decorator with arguments has an extra layer of nested functions. The outer function takes the arguments and returns the actual decorator function, while the inner function takes the original function as an argument and returns the modified function.

Remark that even if we define `repeat_n_times` to have a default value for `n`, when we decorate a function we need to _call_ the decorator, since that returns the actual decorator that we want, namely we need to:

```python
def repeat_n_times(n: int = 3) -> Callable:
    ...

@repeat_n_times()
def say_hello(name: str) -> str:
    return f"Hello {name}!"

@repeat_n_times
def say_goodbye(name: str) -> str:
    return f"Goodbye {name}!"


print(say_hello("Fra"))
# ['Hello Fra!', 'Hello Fra!', 'Hello Fra!']

print(say_goodbye("Fra"))
# <function __main__.repeat_n_times.<locals>.decorator.<locals>.wrapper>
```

Which is not really what we want for the `say_goodbye` function!

Can we do it differently??? Sure we can! And that's how all decorators in **deczoo** are implemented.

## Decorators with arguments, and a trick!

In the [introduction](intro.md) we saw how a decorator is defined, let's stuck to such implementation but let's see how to add additional parameters and control flow without the need to have more level of indentation.

Here is a different implementation of `repeat_n_times`, this time without a triple level of indentation:

```python title="repeat_n_times definition"
from functools import wraps, partial
from typing import Callable

def repeat_n_times(func: Callable = None, n: int = 2) -> Callable:

    @wraps(func)
    def wrapper(*args, **kwargs):

        results = [func(*args, **kwargs) for _ in range(n)]

        return results

    if func is None:
         return partial(repeat_n_times, n=n)
    else:
         return wrapper
```

Let's see what happens here:

- `repeat_n_times` takes as input the function to decorate (`func`) as first argument, and any additional input right after.
- To use this trick, every additional argument must have a default value (which can be `None`).
- Within the decorator we implement a `wrapper` as usual, where we use any additional decorator argument (`n` in this example).
- Since `wrapper` is not run until execution time, we can then check what is the value of `func`:
    - if it is `None`, then it means that only additional arguments have been provided to the decorator, and therefore we return a [partial](https://docs.python.org/3/library/functools.html#functools.partial) decorator with the given arguments that will decorate our function.
    - Otherwise, the function is provided and we return the `wrapper`.

This "trick" allows us to use the decorator with parens, providing custom arguments, or without parens, using defaults, i.e.

```python title="repeat_n_times example"

@repeat_n_times(n=3)  # uses custom argument value
def say_hello(name: str) -> str:
    return f"Hello {name}!"

@repeat_n_times  # uses default argument value
def say_goodbye(name: str) -> str:
    return f"Goodbye {name}!"

print(say_hello("Fra"))
# ["Hello Fra!", "Hello Fra!", "Hello Fra!"]

print(say_goodbye("Fra"))
# ['Goodbye Fra!', 'Goodbye Fra!']
```

Neat! This was possible to achieve using the control flow and `partial` block at the end of the decorator.

Since in [deczoo](../index.md) every decorator is implemented using this strategy, we wrote a sort of "meta-decorator", called [check_parens](../api/utils.md#check_parens) that adds such block to every decorator!

```python
...
if func is None:
    return partial(repeat_n_times, n=n)
else:
    return wrapper
```
