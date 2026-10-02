# _pydoclint_ style violation codes

<!--TOC-->

______________________________________________________________________

**Table of Contents**

- [1. `DOC0xx`: Docstring parsing issues](#1-doc0xx-docstring-parsing-issues)
- [2. `DOC1xx`: Violations about input arguments](#2-doc1xx-violations-about-input-arguments)
  - [2.1. Notes on `DOC103`](#21-notes-on-doc103)
- [3. `DOC2xx`: Violations about return argument(s)](#3-doc2xx-violations-about-return-arguments)
- [4. `DOC3xx`: Violations about class docstring and class constructor](#4-doc3xx-violations-about-class-docstring-and-class-constructor)
- [5. `DOC4xx`: Violations about "yield" statements](#5-doc4xx-violations-about-yield-statements)
- [6. `DOC5xx`: Violations about "raise" and "assert" statements](#6-doc5xx-violations-about-raise-and-assert-statements)
- [7. `DOC6xx`: Violations about class attributes](#7-doc6xx-violations-about-class-attributes)

______________________________________________________________________

<!--TOC-->

______________________________________________________________________

## 1. `DOC0xx`: Docstring parsing issues

| Code     | Explanation                                                                                    |
| -------- | ---------------------------------------------------------------------------------------------- |
| `DOC001` | Potential formatting errors in docstring                                                       |
| `DOC002` | Syntax error in the Python file                                                                |
| `DOC003` | Docstring style mismatch ([explanation](https://jsh9.github.io/pydoclint/style_mismatch.html)) |

## 2. `DOC1xx`: Violations about input arguments

| Code     | Explanation                                                                                                                                                             |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DOC101` | Docstring contains fewer arguments than in function signature                                                                                                           |
| `DOC102` | Docstring contains more arguments than in function signature                                                                                                            |
| `DOC103` | Docstring arguments are different from function arguments. (Or could be other formatting issues: https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103) |
| `DOC104` | Arguments are the same in the docstring and the function signature, but are in a different order.                                                                       |
| `DOC105` | Argument names match, but type hints do not match                                                                                                                       |
| `DOC106` | The option `--arg-type-hints-in-signature` is `True` but there are no argument type hints in the signature                                                              |
| `DOC107` | The option `--arg-type-hints-in-signature` is `True` but not all args in the signature have type hints                                                                  |
| `DOC108` | The option `--arg-type-hints-in-signature` is `False` but there are argument type hints in the signature                                                                |
| `DOC109` | The option `--arg-type-hints-in-docstring` is `True` but there are no type hints in the docstring arg list                                                              |
| `DOC110` | The option `--arg-type-hints-in-docstring` is `True` but not all args in the docstring arg list have type hints                                                         |
| `DOC111` | The option `--arg-type-hints-in-docstring` is `False` but there are type hints in the docstring arg list                                                                |

<a id="notes-on-doc103"></a>

### 2.1. Notes on `DOC103`

Other potential causes to `DOC103` include:

- Numpy docstring style requires this style: `arg1 : int` (a space between
  `arg1` and `:`) but people sometimes write `arg1: int`. This will trigger
  `DOC103`.
- In the Google style, writing an `Args:` section without the preceding summary
  will also trigger `DOC103`.

## 3. `DOC2xx`: Violations about return argument(s)

| Code     | Explanation                                                                                          |
| -------- | ---------------------------------------------------------------------------------------------------- |
| `DOC201` | Function/method does not have a return section in docstring                                          |
| `DOC202` | Function/method has a return section in docstring, but there are no return statements or annotations |
| `DOC203` | Return type(s) in the docstring not consistent with the return annotation                            |

Note on `DOC201`: Methods with `@property` as its outer-most decorator (i.e.,
on the top) do not need to have a return section. Abstract methods and
functions in stub (`.pyi`) files with an `Iterator` or `Iterable` return
annotation don't need one either if their docstring has a "Yields" section:
their bodies are placeholders, so the "Yields" section is what shows that they
yield (rather than returning an iterator).

Note on `DOC203`: For abstract methods and functions in stub (`.pyi`) files
with a `Generator[YieldType, SendType, ReturnType]` return annotation, the
"Returns" section can document either `ReturnType`, as for a generator that has
both "yield" and "return" statements, or the whole annotation, as for a
generator that only yields. Their bodies are placeholders, so they don't show
which one applies.

## 4. `DOC3xx`: Violations about class docstring and class constructor

| Code     | Explanation                                                                                             |
| -------- | ------------------------------------------------------------------------------------------------------- |
| `DOC301` | `__init__()` should not have a docstring; please combine it with the docstring of the class             |
| `DOC302` | The class docstring does not need a "Returns" section, because `__init__()` cannot return anything      |
| `DOC303` | The `__init__()` docstring does not need a "Returns" section, because it cannot return anything         |
| `DOC304` | Class docstring has an argument/parameter section; please put it in the `__init__()` docstring          |
| `DOC305` | Class docstring has a "Raises" section; please put it in the `__init__()` docstring                     |
| `DOC306` | The class docstring does not need a "Yields" section, because `__init__()` cannot yield anything        |
| `DOC307` | The `__init__()` docstring does not need a "Yields" section, because `__init__()` cannot yield anything |

## 5. `DOC4xx`: Violations about "yield" statements

| Code     | Explanation                                                                                                                                                                                                                   |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DOC401` | (Deprecated; this violation code no longer appears)                                                                                                                                                                           |
| `DOC402` | Function/method has "yield" statements, but the docstring does not have a "Yields" section                                                                                                                                    |
| `DOC403` | Function/method has a "Yields" section in the docstring, but there are no "yield" statements, or the return annotation is not a Generator/Iterator/Iterable                                                                   |
| `DOC404` | The types in the docstring's Yields section and the return annotation in the signature are not consistent                                                                                                                     |
| `DOC405` | Function/method has both "return" and "yield" statements; please use `Generator[YieldType, SendType, ReturnType]` as the return annotation ([explanation](https://jsh9.github.io/pydoclint/notes_generator_vs_iterator.html)) |

Note on `DOC403`: It is not reported for abstract methods (methods with
`@abstractmethod` as their outer-most decorator). For functions in stub
(`.pyi`) files, it is only reported when the return annotation isn't a
Generator/Iterator/Iterable (or is missing). The bodies of both are
placeholders, so a body without "yield" statements doesn't mean that the
function doesn't yield anything.

## 6. `DOC5xx`: Violations about "raise" and "assert" statements

| Code     | Explanation                                                                                                                               |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `DOC501` | Function/method has raise statements, but the docstring does not have a "Raises" section                                                  |
| `DOC502` | Function/method has a "Raises" section in the docstring, but there are not "raise" statements in the body                                 |
| `DOC503` | Exceptions in the "Raises" section in the docstring do not match those in the function body                                               |
| `DOC504` | Function/method has assert statements, but the docstring does not have a "Raises" section. (Assert statements could raise "AssertError".) |

Note on `DOC502`: It is not reported for abstract methods (methods with
`@abstractmethod` as their outer-most decorator) or for functions in stub
(`.pyi`) files. Their bodies are placeholders, so a body without "raise"
statements doesn't mean that the function doesn't raise anything.

## 7. `DOC6xx`: Violations about class attributes

| Code     | Explanation                                                                                        |
| -------- | -------------------------------------------------------------------------------------------------- |
| `DOC601` | Class docstring contains fewer class attributes than actual class attributes.                      |
| `DOC602` | Class docstring contains more class attributes than in actual class attributes.                    |
| `DOC603` | Class docstring attributes are different from actual class attributes.                             |
| `DOC604` | Attributes are the same in docstring and class def, but are in a different order.                  |
| `DOC605` | Attribute names match, but type hints in these attributes do not match                             |
| `DOC606` | This attribute is documented inline, but it should be documented in the class docstring instead    |
| `DOC607` | The class docstring should not have an "Attributes" section; please document all attributes inline |

More about checking class attributes:
https://jsh9.github.io/pydoclint/checking_class_attributes.html
