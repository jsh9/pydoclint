# Notes on `Generator` vs `Iterator`

<!--TOC-->

______________________________________________________________________

**Table of Contents**

- [1. Functions that both yield and return](#1-functions-that-both-yield-and-return)
- [2. Which return annotations count as generators or iterators](#2-which-return-annotations-count-as-generators-or-iterators)

______________________________________________________________________

<!--TOC-->

## 1. Functions that both yield and return

Most likely, you landed on this page because you saw a `DOC405` violation:

> DOC405: Method `myMethod` has both "return" and "yield" statements. Please
> use Generator[YieldType, SendType, ReturnType] as the return type annotation,
> and put your yield type in YieldType and return type in ReturnType.

If you are trying to write functions that both yield and return something, such
as this one:

```python
from typing import Generator

def echo_round() -> Generator[int, float, str]:
    sent = yield 0
    while sent >= 0:
        sent = yield round(sent)  # round() returns int
    return 'Done'
```

the most appropriate return type annotation would be a `Generator`.

According to Python's official documentation
(https://docs.python.org/3/library/typing.html#typing.Generator), the three
components of a `Generator` type annotation are:

- Yield type
- Send type
- Return type

Therefore, the recommended way to specify the return type annotation is like
what the example above shows. And the recommended way to write the docstring is
to use both a "Yields" section and a "Return" section to document the yield and
return values/types.

## 2. Which return annotations count as generators or iterators

Some checks depend on whether the return annotation is a generator or an
iterator: whether a "Returns" section is needed (`DOC201`), whether a "Yields"
section is allowed (`DOC403`), and which type the "Yields" section should have
(`DOC404`). _pydoclint_ decides this by the last name in the return annotation,
which has to be exactly `Generator`, `AsyncGenerator`, `Iterator`, `Iterable`,
`AsyncIterator`, or `AsyncIterable`.

These are all recognized, with or without `[...]`:

- `Iterator[int]`, after `from typing import Iterator` or
  `from collections.abc import Iterator`
- `typing.Iterator[int]`, after `import typing`
- `collections.abc.Iterator[int]`, after `import collections.abc`
- `t.Iterator[int]`, after `import typing as t`

These are not recognized:

- Unions and `Optional`, such as `Iterator[int] | None` or
  `Optional[Iterator[int]]`. A function with "yield" statements always returns
  a generator object and never `None`, so leave out the `None` part.
- Other wrapped annotations, such as `Annotated[Iterator[int], ...]`
- Quoted annotations (forward references), such as `"Iterator[int]"`
- Renamed imports, such as `It[int]` after `from typing import Iterator as It`
  (see
  [cases that _pydoclint_ is not designed to handle](https://jsh9.github.io/pydoclint/notes_for_users.html#1-cases-that-pydoclint-is-not-designed-to-handle))
- Names that only start with one of the six names, such as `IterableDataset`

_pydoclint_ doesn't resolve imports, so it only looks at the name. A class from
another library that happens to be named `Generator`, such as
`numpy.random.Generator`, is treated like `typing.Generator`. A missing
"Returns" section for such a function may then go unreported, especially in
stub (`.pyi`) files.
