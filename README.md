# pydoclint

A Python docstring linter to check whether a docstring's sections (arguments, returns, raises, ...) match the function signature or function implementation.

It runs really fast. In fact, it is at least 30,000 times faster than [darglint](https://github.com/terrencepreilly/darglint) (another linter of the same purposes which is no longer maintained).

Here is a comparison of running time on some famous Python projects:

|                                                              | pydoclint | darglint             |
| ------------------------------------------------------------ | --------- | -------------------- |
| [numpy](https://github.com/numpy/numpy)                      | 0.08 sec  | > 40 min (> 30,000x) |
| [scikit-learn](https://github.com/scikit-learn/scikit-learn) | 0.09 sec  | > 40 min (> 30,000x) |

Currently, `pydoclint` only works when you write your docstrings in the [numpy stlyle](https://numpydoc.readthedocs.io/en/latest/format.html). Support for the [Google style](https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html) docstrings will be added soon.

**Note**: this linter and [pydocstyle](https://github.com/PyCQA/pydocstyle) serves complementary purposes. It is recommended that you use both together.

## 1. Installation

```
pip install pydoclint
```

Note that `pydoclint` only supports Python 3.8 and above.

## 2. Usage

### 2.1. As a standalone command line tool

```
pydoclint <FILE_OR_FOLDER>
```

Replace `<FILE_OR_FOLDER>` with the file/folder names you want, such as `.`.

### 2.2. As a flake8 plugin

Once you install `pydoclint` you will have also installed `flake8`. Then you can run:

```
flake8 --select=DOC <FILE_OR_FOLDER>
```

If you don't include `--select=DOC` in your command, `flake8` will also run other built-in flake8 linters on your code.

## 3. Style violation codes

`pydoclint` currently has the following style violation codes:

### 3.1. `DOC1xx`: Violations about input arguments

| Code     | Explanation                                                                                                                                    |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `DOC101` | Docstring contains fewer arguments than in function signature                                                                                  |
| `DOC102` | Docstring contains more arguments than in function signature                                                                                   |
| `DOC103` | Docstring arguments are different from function arguments. (Or did you miss the space between the argument name and the ":" in the docstring?) |
| `DOC104` | Arguments are the same in the docstring and the function signature, but are in a different order.                                              |
| `DOC105` | Argument names match, but type hints do not match                                                                                              |

### 3.2. `DOC2xx`: Violations about return argument(s)

| Code     | Explanation                                                                                          |
| -------- | ---------------------------------------------------------------------------------------------------- |
| `DOC201` | Function/method does not have a return section in docstring                                          |
| `DOC202` | Function/method has a return section in docstring, but there are no return statements or annotations |

### 3.3. `DOC3xx`: Violations about class docstring and class constructor

| Code     | Explanation                                                                                 |
| -------- | ------------------------------------------------------------------------------------------- |
| `DOC301` | `__init__()` should not have a docstring; please combine it with the docstring of the class |
| `DOC302` | The docstring for the class does not need a "Returns" sections                              |

### 3.4. `DOC4xx`: Violations about "yield" statements

| Code     | Explanation                                                                                                                   |
| -------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `DOC401` | Function/method returns a Generator, but the docstring does not have a "Yields" section                                       |
| `DOC402` | Function/method has "yield" statements, but the docstring does not have a "Yields" section                                    |
| `DOC403` | Function/method has a "Yields" section in the docstring, but there are no "yield" statements or a Generator return annotation |

### 3.5. `DOC5xx`: Violations about "raise" statements

| Code     | Explanation                                                                                               |
| -------- | --------------------------------------------------------------------------------------------------------- |
| `DOC501` | Function/method has "raise" statements, but the docstring does not have a "Raises" section                |
| `DOC502` | Function/method has a "Raises" section in the docstring, but there are not "raise" statements in the body |

## 4. Configuration options

There are several configuration options available. They can be used invidually or together.

### 4.1. `--check-type-hint` (shortform: `-th`, default: `True`)

If `True`, the type hints in the docstring and in the Python code need to exactly match.

To turn this optoin on/off, do this:

```
pydoclint --check-type-hint=False <FILE_OR_FOLDER>
```

or

```
flake8 --check-type-hint=False <FILE_OR_FOLDER>
```

### 4.2. `--check-arg-order` (shortform: `-ao`, default: `True`)

If `True`, the input argument order in the docstring needs to match that in the function signature.

To turn this optoin on/off, do this:

```
pydoclint --check-arg-order=False <FILE_OR_FOLDER>
```

or

```
flake8 --check-arg-order=False <FILE_OR_FOLDER>
```

### 4.3. `--skip-checking-short-docstrings` (shortform: `-scsd`, default: `True`)

If `True`, `pydoclint` won't check functions that have only a short description in their docstring.

To turn this optoin on/off, do this:

```
pydoclint --skip-checking-short-docstrings=False <FILE_OR_FOLDER>
```

or

```
flake8 --skip-checking-short-docstrings=False <FILE_OR_FOLDER>
```

### 4.4. `--skip-checking-raises` (shortform: `-scr`, default: `False`)

If `True`, `pydoclint` won't report `DOC501` or `DOC502` if there are `raise` statements in the function/method but there aren't any "raises" sections in the docstring (or vice versa).
