# Notes for users

<!--TOC-->

______________________________________________________________________

**Table of Contents**

- [1. Cases that _pydoclint_ is not designed to handle](#1-cases-that-pydoclint-is-not-designed-to-handle)
- [2. Notes on writing type hints](#2-notes-on-writing-type-hints)
- [3. How to integrate _pydoclint_ with different editors or IDEs](#3-how-to-integrate-pydoclint-with-different-editors-or-ides)
  - [3.1. Integrate _pydoclint_ with Neovim using null-ls](#31-integrate-pydoclint-with-neovim-using-null-ls)

______________________________________________________________________

<!--TOC-->

## 1. Cases that _pydoclint_ is not designed to handle

_pydoclint_ uses a static syntax analyzer (Python's
[official AST module](https://docs.python.org/3/library/ast.html)) to analyze
the incoming Python source code, and
[docstring_parser_fork](https://github.com/jsh9/docstring_parser_fork) to parse
docstrings. It never imports or runs your code.

The static syntax analysis is very fast because it doesn't execute or evaluate
any code. For example, this piece of Python code is not runnable:

```python
a = b
```

because `b` is not defined. But the static syntax analyzer does not "know"
this: it doesn't need to "know" this to analyze the syntactic structure of
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

## 2. Notes on writing type hints

As mentioned in Section 1 above, _pydoclint_ uses static syntax analysis. As a
result, it cannot really "know" that these type annotations are in fact
equivalent:

| Type annotation   | Equivalent version |
| ----------------- | ------------------ |
| `Optional[str]`   | `str \| None`      |
| `Union[str, int]` | `int \| str`       |
| `Tuple[str, int]` | `tuple[str, int]`  |

Additionally, _pydoclint_ does not recognize some docstring conventions allowed
in the docstring style guide, such as using "`int, optional`" for
`Optional[int]`.

Right now, the only way to make _pydoclint_ stop reporting style violations is
to make sure the docstring type annotations match the signature type
annotations verbatim.

Again, the authors of _pydoclint_ feel that this is a reasonable price to pay
in order to achieve fast linting and reduce ambiguity.

## 3. How to integrate _pydoclint_ with different editors or IDEs

### 3.1. Integrate _pydoclint_ with Neovim using null-ls

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

Adjust `extra_args` based on your preferred _pydoclint_ configuration. With
this setup, you can now enjoy the benefits of _pydoclint_'s fast and
comprehensive docstring linting directly within your Neovim editing
environment.
