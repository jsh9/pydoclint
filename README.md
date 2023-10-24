# pydoclint

_Pydoclint_ is a Python docstring linter to check whether a docstring's
sections (arguments, returns, raises, ...) match the function signature or
function implementation.

It runs really fast. In fact, it can be thousands of times faster than
[darglint](https://github.com/terrencepreilly/darglint) (or its maintained fork
[darglint2](https://github.com/akaihola/darglint2)).

Here is a comparison of linting time on some famous Python projects:

|                                                              | pydoclint | darglint                          |
| ------------------------------------------------------------ | --------- | --------------------------------- |
| [numpy](https://github.com/numpy/numpy)                      | 2.0 sec   | 49 min 9 sec (1,475x slower)      |
| [scikit-learn](https://github.com/scikit-learn/scikit-learn) | 2.4 sec   | 3 hr 5 min 33 sec (4,639x slower) |

Additionally, _pydoclint_ can detect some quite a few style violations that
darglint cannot.

Currently, _pydoclint_ supports three docstring styles:
[numpy](https://numpydoc.readthedocs.io/en/latest/format.html),
[Google](https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html),
and
[Sphinx](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html).

Another note: this linter and [pydocstyle](https://github.com/PyCQA/pydocstyle)
serves complementary purposes. It is recommended that you use both together.

The full documentation of _pydoclint_ (including this README) can be found
here: [https://jsh9.github.io/pydoclint](https://jsh9.github.io/pydoclint)

The corresponding Github repository of _pydoclint_ is:
[https://github.com/jsh9/pydoclint](https://github.com/jsh9/pydoclint)

---

**Table of Contents**

<!--TOC-->

- [1. Installation](#1-installation)
- [2. Usage](#2-usage)
  - [2.1. As a native command line tool](#21-as-a-native-command-line-tool)
  - [2.2. As a _flake8_ plugin](#22-as-a-flake8-plugin)
  - [2.3. As a pre-commit hook](#23-as-a-pre-commit-hook)
  - [2.4. Native vs _flake8_](#24-native-vs-flake8)
  - [2.5. How to configure _pydoclint_](#25-how-to-configure-pydoclint)
  - [2.6. How to ignore certain violations in _flake8_ mode](#26-how-to-ignore-certain-violations-in-flake8-mode)
- [3. Style violation codes](#3-style-violation-codes)
- [4. Notes for users](#4-notes-for-users)
- [5. Notes for developers](#5-notes-for-developers)

<!--TOC-->

## 1. Installation

To install only the native _pydoclint_ tooling, run this command:

```
pip install pydoclint
```

To use _pydoclint_ as a _flake8_ plugin, please run this command, which will
also install _flake8_ to the current Python environment:

```
pip install pydoclint[flake8]
```

Note that _pydoclint_ currently only supports Python 3.8 and above. (Python 3.7
support may be added if there are interests and requests.)

## 2. Usage

### 2.1. As a native command line tool

```
pydoclint <FILE_OR_FOLDER>
```

Replace `<FILE_OR_FOLDER>` with the file/folder names you want, such as `.`.

### 2.2. As a _flake8_ plugin

Once you install _pydoclint_ you will have also installed _flake8_. Then you
can run:

```
flake8 --select=DOC <FILE_OR_FOLDER>
```

If you don't include `--select=DOC` in your command, _flake8_ will also run
other built-in _flake8_ linters on your code.

### 2.3. As a pre-commit hook

_pydoclint_ is configured for [pre-commit](https://pre-commit.com/) and can be
set up as a hook with the following `.pre-commit-config.yaml` configuration:

```yaml
- repo: https://github.com/jsh9/pydoclint
  rev: <latest_tag>
  hooks:
    - id: pydoclint
      args: [--style=google, --check-return-types=False]
```

You will need to install `pre-commit` and run `pre-commit install`.

### 2.4. Native vs _flake8_

Should I use _pydoclint_ as a native command line tool or a _flake8_ plugin?
Here's comparison:

|                 | Pros                                     | Cons                                                          |
| --------------- | ---------------------------------------- | ------------------------------------------------------------- |
| Native tool     | Slightly faster; supports "baseline" [*] | No inline or project-wide omission support right now [**]     |
| _flake8_ plugin | Supports inline or project-wide omission | Slightly slower because other flake8 plugins are run together |

\*) "Baseline" allows you to log the current violation state of your existing
project, making adoption of _pydoclint_ much easier.

\*\*) This feature may be added in the near future

### 2.5. How to configure _pydoclint_

Please read this page:
[How to configure _pydoclint_](https://jsh9.github.io/pydoclint/how_to_config.html)

### 2.6. How to ignore certain violations in _flake8_ mode

Please read this page:
[How to ignore certain violations](https://jsh9.github.io/pydoclint/how_to_ignore.html)

## 3. Style violation codes

_pydoclint_ currently has 6 categories of style violation codes:

- `DOC0xx`: Docstring parsing issues
- `DOC1xx`: Violations about input arguments
- `DOC2xx`: Violations about return argument(s)
- `DOC3xx`: Violations about class docstring and class constructor
- `DOC4xx`: Violations about "yield" statements
- `DOC5xx`: Violations about "raise" statements

For detailed explanations of each violation code, please read this page:
[_pydoclint_ style violation codes](https://jsh9.github.io/pydoclint/violation_codes.html).

## 4. Notes for users

If you'd like to use _pydoclint_ for your project, it is recommended that you
read these additional notes
[here](https://jsh9.github.io/pydoclint/notes_for_users.html).

Specifically, there is a section in the additional notes on how to easily adopt
_pydoclint_ for existing legacy projects.

## 5. Notes for developers

If you'd like to contribute to the code base of _pydoclint_, thank you!

[This guide](https://jsh9.github.io/pydoclint/notes_for_developers.html) can
hopefully help you get familiar with the code base faster.
