<img src="img/deczoo-logo.png" width=185 height=185 align="right">

![](https://img.shields.io/github/license/FBruzzesi/deczoo)
<img src ="img/interrogate-shield.svg">
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
<img src ="img/coverage.svg">
<img src = "https://img.shields.io/pypi/pyversions/deczoo">


# Deczoo

> A zoo for decorators

There are many great decorators out there that we use everyday. Why don't collect a few of them?

I found myself implementing over and over some common decorators in different projects.
The hope is to gather them here and use this codebase.

---

[Documentation](https://fbruzzesi.github.io/deczoo) | [Source Code](https://github.com/fbruzzesi/deczoo)

---

## Alpha Notice

This codebase is experimental and is working for my use cases. It is very probable that there are cases not covered and for which it breaks (badly). If you find them, please feel free to open an issue in the [issue page](https://github.com/FBruzzesi/deczoo/issues) of the repo.

## What is a decorator?

In short a python decorator is a way to modify or enhance the behavior of a function or a class without actually modifying the source code of the function or class.

Decorators are implemented as functions (or classes) that take a function or a class as input and return a new function or class that has some additional functionality.

To have a more in-depth explanation you can check the [next section](decorators/intro.md).

## Installation

**deczoo** is published as a Python package on [pypi](https://pypi.org/), and it can be installed with pip, directly from source using git, or with a local clone:

=== "pip (pypi)"

    ```bash
    python -m pip install deczoo
    ```

=== "source/git"

    ```bash
    python -m pip install git+https://github.com/FBruzzesi/deczoo.git
    ```

=== "local clone"

    ```bash
    git clone https://github.com/FBruzzesi/deczoo.git
    cd deczoo
    python -m pip install .
    ```

### Dependencies

As of now, the library has no additional required dependencies, however:

- some functionalities works only on UNIX systems (`@memory_limit` and `@timeout`)
- to use some decorators you may need to install additional dependencies (e.g. install [`chime`](https://github.com/MaxHalford/chime) to use `@chime_on_end`)

## License

The project has a [MIT Licence](https://github.com/FBruzzesi/deczoo/blob/main/LICENSE)
