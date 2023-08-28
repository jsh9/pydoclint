# Notes for users

**Table of Contents**

<!--TOC-->

- [1. Why is _pydoclint_ so much faster than _darglint_](#1-why-is-pydoclint-so-much-faster-than-darglint)
- [2. Cases that _pydoclint_ is not designed to handle](#2-cases-that-pydoclint-is-not-designed-to-handle)
- [3. Notes on writing type hints](#3-notes-on-writing-type-hints)

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
