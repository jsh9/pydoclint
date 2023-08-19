# Notes on `Generator` vs `Iterator`

Most likely, you landed on this page because you saw a `DOC405` violation:

> DOC405: Method `myMethod` has "yield" statements, but the return signature is
> `Iterator`. Please use `Generator` instead.

This is because _pydoclint_ uses the following criteria:

- If the return annotation in the signature is `Generator` or `AsyncGenerator`,
  there should be a "Yields" section in the docstring
- If the return annotation in the signature is `Iterator`, `AsyncIterator`,
  `Iterable`, or `AsyncIterable`, there should be a "Returns" section in the
  docstring

Here is the rationale behind:

Firstly, `(Async)Generator` is a sub type of `(Async)Iterator/ble`:

```python
>>> from typing import Iterator, Iterable, Generator
>>> issubclass(Generator, Iterator)
True
>>> issubclass(Iterator, Generator)
False
>>> issubclass(Generator, Iterable)
True
>>> issubclass(Iterable, Generator)
False
```

Secondly, when we use `yield` statements in a function body, what's yielded is
always a `Generator`. But sometimes, we can explicitly return iterators, and
they are not generators:

```python
from typing import (
    Any,
    Iterator,
    Tuple,
    List,
)

def zip_lists(
        list1: List[Any],
        list2: List[Any],
) -> Iterator[Tuple[Any, Any]]:
    return zip(list1, list2)
```

Additionally, people can use `return` and `yield` statements in the same
function. Although this may not be the best practice, but it is not a syntax
error.

This means that the **_only_** way to tell whether the docstring should have a
"Returns" or a "Yields" section is by looking at the function signature's
return annotation:

- `Generator`: it should have a "Yields" section
- `Iterator`: it should have a "Returns" section
