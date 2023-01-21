# Example Usage

##  call_counter

Counts how many times a function has been called, stores such values in the `_calls` attribute.

```python
from deczoo import call_counter

@call_counter
def add(a, b):
    return a+b

for _ in range(3):
    add(1,2)

add._calls
3
```

##  `catch`

Wraps a function in a try-except block, potentially prevent exception to be raised and return a custom value or raises custom exception.

```python
from deczoo import catch

@catch(return_on_exception=-999)
def add(a, b):
    return a+b

add(1, 2)
3

add(1, "a")
-999
```

##  `check_args`
Checks that function arguments satisfy given rules.

```python
from deczoo import check_args

@check_args(a=lambda t: t>0)
def add(a, b):
    return a+b

add(1,2)
3

add(-2, 2)
# ValueError: Argument a doesn't satisfy its rule
```

##  `chime_on_end`

Notify with chime sound whenever the function ends

```python
from deczoo import chime_on_end

@chime_on_end(theme="mario")
def add(a, b):
    return a+b

_ = add(1, 2)
# you should hear a sound now!
```

##  `dump_result`

Saves function result in a pickle file, eventually creates a results folder if doesn't exist.

```python
from deczoo import dump_result

@dump_result(include_args=True)
def add(a, b):
    return a+b

_ = add(1, 2)# will save the result in results/add_1_2_%Y%m%d_%H%M%S.pickle
```

##  `log`
Tracks function time taken, arguments and errors

```python
from deczoo import log

@log
def add(a, b):
    return a+b

_ = add(1, 2)
# add args=(a=1, b=2) time=0:00:00.000111
```

##  `timer`
Tracks function time taken, to be honest this is nothing more than
```python
from functools import partial

timer = partial(log, log_time=True, log_args=False, log_error=False)
```

##  `memory_limit`
Sets a memory limit for a function

```python
from deczoo import memory_limit

@memory_limit(percentage=0.2)
def limited():
    for i in list(range(10 ** 8)):
        _ = 1 + 1
    return "done"

def unlimited():
    for i in list(range(10 ** 8)):
        _ = 1 + 1
    return "done"

limited()
# MemoryError: Reached memory limit

unlimited()
done
```

##  `retry`
Wraps a function with a retry block

```python
from deczoo import retry

@retry(n_tries=2, delay=1.)
def add(a, b): return a+b

_ = add(1, 2)
# Attempt 1/2: Successed

_ = add(1, "a")
# Attempt 1/2: Failed with error: unsupported operand type(s) for +: 'int' and 'str'
# Attempt 2/2: Failed with error: unsupported operand type(s) for +: 'int' and 'str'
```

##  `timeout`

Sets a time limit to a function, terminates the process if it hasn't finished within such time limit.
Remark that it uses the signal library (https://docs.python.org/3/library/signal.html) which fully supported only on UNIX.

```python
import time
from deczoo import timeout

@timeout(time_limit=3)
def add(a, b):
    time.sleep(2)
    return a+b

add(1, 2)
3

@timeout(time_limit=1)
def add(a, b):
    time.sleep(2)
    return a+b

add(1, 2)
# Exception: Reached time limit, terminating add
```
