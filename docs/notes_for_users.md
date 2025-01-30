# Notes for users

**Table of Contents**

<!--TOC-->

- [1. Why is _pydoclint_ so much faster than _darglint_](#1-why-is-pydoclint-so-much-faster-than-darglint)
- [2. Cases that _pydoclint_ is not designed to handle](#2-cases-that-pydoclint-is-not-designed-to-handle)
- [3. Notes on writing type hints](#3-notes-on-writing-type-hints)
- [4. Notes on writing Sphinx-style docstrings](#4-notes-on-writing-sphinx-style-docstrings)
- [5. Notes for Google-style users](#5-notes-for-google-style-users)
- [6. Notes for Numpy-style users](#6-notes-for-numpy-style-users)
- [7. How to adopt _pydoclint_ more easily in legacy projects](#7-how-to-adopt-pydoclint-more-easily-in-legacy-projects)
- [8. How to integrate _pydoclint_ with different editors or IDEs](#8-how-to-integrate-pydoclint-with-different-editors-or-ides)
  - [8.1. Integrate _pydoclint_ with Neovim using null-ls](#81-integrate-pydoclint-with-neovim-using-null-ls)

<!--TOC-->

## 1. Why is _pydoclint_ so much faster than _darglint_

Based on the best understanding of the authors of _pydoclint_, here are some
reasons (this may not be an exhaustive list):

- _pydoclint_ uses reputable docstring parsers:
  [docstring_parser](https://github.com/rr-/docstring_parser), while _darglint_
  implements
  [its own docstring parser](https://github.com/terrencepreilly/darglint/tree/abc26b768cd7135d848223ba53f68323593c33d5/darglint/parse)
- _pydoclint_ uses a static syntax analyzer: Python's
  [official AST module](https://docs.python.org/3/library/ast.html)
  - On the other hand _darglint_ uses
    [Python's `inspect` module](https://github.com/search?q=repo%3Aterrencepreilly%2Fdarglint%20inspect&type=code)
    in some places. (The `inspect` module requires compiling the Python source
    code, which can be time consuming for big code bases)
  - This choice of _pydoclint_ is not without caveats -- please read Section 2

## 2. Cases that _pydoclint_ is not designed to handle

_pydoclint_ uses a static syntax analyzer (Python's
[official AST module](https://docs.python.org/3/library/ast.html)) to analyze
the incoming Python source code.

The static syntax analysis is very fast because it doesn't execute or evaluate
any code. For example, this piece of Python code is not runnable:

```python
a = b
```

because `b` is not defined. But the static syntax analyzer does not "know"
this: it doesn't need to "know" this to analyze the syntatic structure of
`a = b`.

As a result, _pydoclint_ is not designed to handle cases where Pythonic naming
conventions are broken, such as:

- Renaming `classmethod` to something like `hello`:

```python
hello = classmethod

class MyClass:
    @hello
    def myClassMethod(cls):
        pass
```

- Renaming `staticmethod` to something else, similar to the `classmethod` case
  above
- Use names other than `self` or `cls` in methods, such as:

```python
class MyClass:
    def myMethod(hello, arg1):  # the 1st argument is `self` by convention
        pass

    @classmethod
    def myClassMethod(hey, arg2):  # the 1st argument is `cls` by convention
        pass
```

- Renaming type annotations into other names in the code but not in the
  docstring:

```python
from typing import List as hello
from typing import Optional as world

def myFunc(arg1: hello[int], arg2: world[str]) -> None:
    """
    An example function.

    pydoclint expects consistency between signature type annotation (`hello[int]`)
    and docstring type annotation (`List[int]`).

    Parameters
    ----------
    arg1 : List[int]
        Arg 1
    arg2 : world[str]
        Arg 2
    """
    print(arg1, arg2)
```

The authors of _pydoclint_ feel that this is a sensible design choice to
achieve and maintain _pydoclint_'s speed.

## 3. Notes on writing type hints

As mentioned in Section 2 above, _pydoclint_ uses static syntax analysis. As a
result, it cannot really "know" that these type annotations are in fact
equivalent:

| Type annotation   | Equivalent version |
| ----------------- | ------------------ | ----- |
| `Optional[str]`   | `str               | None` |
| `Union[str, int]` | `int               | str`  |
| `Tuple[str, int]` | `tuple[str, int]`  |

Additionally, _pydoclint_ does not recognize some docstring conventions allowed
in the docstring style guide, such as using "`int, optional`" for
`Optional[int]`.

Right now, the only way to make _pydoclint_ stop reporting style violations is
to make sure the docstring type annotations match the signature type
annotations verbatim.

Again, the authors of _pydoclint_ feel that this is a reasonable price to pay
in order to achieve fast linting and reduce ambiguity.

## 4. Notes on writing Sphinx-style docstrings

The
[official Sphinx documentation](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html)
does not explicitly state this, so it is unclear what header to use to specify
the type of what a function yields.

Many people use `rtype`, but the authors of _pydoclint_ find it difficult to
differentiate the type of return value and the type of yield value.

Therefore, _pydoclint_ expects the convention of `ytype` for yield types. This
is actually common practice, as evident from a code search on GitHub:
https://github.com/search?q=%3Aytype%3A+language%3APython&type=code&l=Python

## 5. Notes for Google-style users

By default, _pydoclint_ checks return type and yield type consistencies, and it
also requires argument types in the docstring. In other words, by _pydoclint_'s
default, this is an acceptable Google-style docstring:

```python
"""
This is a function.

Args:
    arg1 (int): Arg 1
    arg2 (float): Arg 2
    arg3 (Optional[Union[float, int, str]]): Arg 3

Returns:
    int: Result
"""
```

However, this may not be the convention of a lot of Google-style docstring
writers.

But do not worry: here are some config options to tweak:

- `--arg-type-hints-in-docstring`: you can set it to `False`
- `--check-return-types`: you can set it to `False`
- `--check-yield-types`: you can set it to `False`

[Here](https://jsh9.github.io/pydoclint/config_options.html) are all the
configurable options of _pydoclint_, and
[here](https://jsh9.github.io/pydoclint/how_to_config.html) is how to configure
_pydoclint_.

## 6. Notes for Numpy-style users

The numpy style guide specifies a few different ways to include default values for
function args in the the docstring. The following styles are currently supported.
For a function with a signature like:

```python
def some_fn(arg1: int = 10):
```

The Parameter block of the doc string should use on of these formats:
```python
    Parameters
    ----------
    arg1 : int, default 10
OR
    arg1 : int, default is 10
OR
    arg1 : int, default: 10
OR
    arg1 : int = 10

```

The portion following the type hints are ignored and not checked for congruence with the
function signature.

## 7. How to adopt _pydoclint_ more easily in legacy projects

If you have large legacy projects, adoting a new linter may be daunting: you'll
see hundreds or even thousands of violations at first.

Fortunately, _pydoclint_ offers a "baseline" feature, which ignores existing
violations for now, and will only report new violations.

To use this feature, you only need to generate a "baseline violations" file
(containing the hundreds or thousands of existing violations) once, and save it
somewhere in your repo.

For more details, please check out
[this section](https://jsh9.github.io/pydoclint/config_options.html#12---baseline).

## 8. How to integrate _pydoclint_ with different editors or IDEs

### 8.1. Integrate _pydoclint_ with Neovim using null-ls

If you use [Neovim](https://neovim.io/), you can integrate _pydoclint_ with
your editor using the [null-ls](https://github.com/nvimtools/none-ls.nvim)
plugin. null-ls allows you to use linters and formatters in Neovim in a simple
and efficient way. First, make sure you have installed null-ls using your
preferred package manager. Next, add the following configuration to your Neovim
config file to register _pydoclint_ as a diagnostic source:

```lua
local null_ls = require("null-ls")

null_ls.setup({
    sources = {
        null_ls.builtins.diagnostics.pydoclint,
    },
})
```

This will enable _pydoclint_ to provide diagnostic messages for your Python
code directly in Neovim. You can further customize the behavior of _pydoclint_
by passing additional options:

```lua
local null_ls = require("null-ls")

null_ls.setup({
    sources = {
        null_ls.builtins.diagnostics.pydoclint.with({
            extra_args = {"--style=google", "--check-return-types=False"},
        }),
    },
})
```

Adjust the extra*args based on your preferred \_pydoclint* configuration. With
this setup, you can now enjoy the benefits of _pydoclint_'s fast and
comprehensive docstring linting directly within your Neovim editing
environment.
