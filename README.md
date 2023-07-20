# pydoclint

A Python docstring linter to check whether a docstring's sections (arguments,
returns, raises, ...) match the function signature or function implementation.

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

- The [numpy stlyle](https://numpydoc.readthedocs.io/en/latest/format.html)
- The
  [Google style](https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html)
- The
  [Sphinx style](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html)

Another note: this linter and [pydocstyle](https://github.com/PyCQA/pydocstyle)
serves complementary purposes. It is recommended that you use both together.

**Table of Contents**

<!--TOC-->

- [1. Installation](#1-installation)
- [2. Usage](#2-usage)
  - [2.1. As a native command line tool](#21-as-a-native-command-line-tool)
  - [2.2. As a _flake8_ plugin](#22-as-a-_flake8_-plugin)
  - [2.3. As a pre-commit hook](#23-as-a-pre-commit-hook)
  - [2.4. Native vs _flake8_](#24-native-vs-_flake8_)
  - [2.5. Configuration](#25-configuration)
    - [2.5.1. Setting options inline](#251-setting-options-inline)
    - [2.5.2. Setting options in a configuration file](#252-setting-options-in-a-configuration-file)
- [3. Style violation codes](#3-style-violation-codes)
  - [3.0. `DOC0xx`: Docstring parsing issues](#30-doc0xx-docstring-parsing-issues)
  - [3.1. `DOC1xx`: Violations about input arguments](#31-doc1xx-violations-about-input-arguments)
    - [Notes on `DOC103`:](#notes-on-doc103)
  - [3.2. `DOC2xx`: Violations about return argument(s)](#32-doc2xx-violations-about-return-arguments)
  - [3.3. `DOC3xx`: Violations about class docstring and class constructor](#33-doc3xx-violations-about-class-docstring-and-class-constructor)
  - [3.4. `DOC4xx`: Violations about "yield" statements](#34-doc4xx-violations-about-yield-statements)
  - [3.5. `DOC5xx`: Violations about "raise" statements](#35-doc5xx-violations-about-raise-statements)
- [4. Additional notes](#4-additional-notes)

<!--TOC-->

## 1. Installation

```
pip install pydoclint
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
      args:
        - "--config=pyproject.toml"
```

You will need to install `pre-commit` and run `pre-commit install`.

### 2.4. Native vs _flake8_

Should I use _pydoclint_ as a native command line tool or a _flake8_ plugin?
Here's comparison:

|                 | Pros                                     | Cons                                                          |
| --------------- | ---------------------------------------- | ------------------------------------------------------------- |
| Native tool     | Slightly faster                          | No inline or project-wide omission support right now [*]      |
| _flake8_ plugin | Supports inline or project-wide omission | Slightly slower because other flake8 plugins are run together |

\*) This feature may be added in the near future

### 2.5. Configuration

Here is how to configure _pydoclint_. For detailed explanations of all options,
please read [this page](https://jsh9.github.io/pydoclint/config_options.html).

#### 2.5.1. Setting options inline

- Native:

  ```bash
  pydoclint --check-arg-order=False <FILE_OR_FOLDER_PATH>
  ```

- Flake8:

  ```bash
  flake8 --check-arg-order=False <FILE_OR_FOLDER_PATH>
  ```

#### 2.5.2. Setting options in a configuration file

- Native:

  - In a `.toml` file somewhere in your project folder, add a section like this
    (put in the config that you need):

    ```toml
    [tool.pydoclint]
    style = 'google'
    exclude = '\.git|\.tox|tests/data|some_script\.py'
    require-return-section-when-returning-none = true
    ```

  - Then, specify the path of the `.toml` file in your command:

    ```bash
    pydoclint --config=path/to/my/config.toml <FILE_OR_FOLDER_PATH>
    ```

- Flake8:
  - In your flake8 config file (see
    [flake8's official doc](https://flake8.pycqa.org/en/latest/user/configuration.html#configuration-locations)),
    add the config you need under the section `[flake8]`

## 3. Style violation codes

_pydoclint_ currently has the following style violation codes:

### 3.0. `DOC0xx`: Docstring parsing issues

| Code     | Explanation                              |
| -------- | ---------------------------------------- |
| `DOC001` | Potential formatting errors in docstring |

### 3.1. `DOC1xx`: Violations about input arguments

| Code     | Explanation                                                                                                                                         |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DOC101` | Docstring contains fewer arguments than in function signature                                                                                       |
| `DOC102` | Docstring contains more arguments than in function signature                                                                                        |
| `DOC103` | Docstring arguments are different from function arguments. (Or could be other formatting issues: https://github.com/jsh9/pydoclint#notes-on-doc103) |
| `DOC104` | Arguments are the same in the docstring and the function signature, but are in a different order.                                                   |
| `DOC105` | Argument names match, but type hints do not match                                                                                                   |
| `DOC106` | The option `--arg-type-hints-in-signature` is `True` but there are no argument type hints in the signature                                          |
| `DOC107` | The option `--arg-type-hints-in-signature` is `True` but not all args in the signature have type hints                                              |
| `DOC108` | The option `--arg-type-hints-in-signature` is `False` but there are argument type hints in the signature                                            |
| `DOC109` | The option `--arg-type-hints-in-docstring` is `True` but there are no type hints in the docstring arg list                                          |
| `DOC110` | The option `--arg-type-hints-in-docstring` is `True` but not all args in the docstring arg list have type hints                                     |
| `DOC111` | The option `--arg-type-hints-in-docstring` is `False` but there are type hints in the docstring arg list                                            |

#### Notes on `DOC103`:

Other potential causes to `DOC103` include:

- Numpy docstring style requires this style: `arg1 : int` (a space between
  `arg1` and `:`) but people sometimes write `arg1: int`. This will trigger
  `DOC103`.
- In the Google style, writing an `Args:` section without the preceding summary
  will also trigger `DOC103`.

### 3.2. `DOC2xx`: Violations about return argument(s)

| Code     | Explanation                                                                                          |
| -------- | ---------------------------------------------------------------------------------------------------- |
| `DOC201` | Function/method does not have a return section in docstring                                          |
| `DOC202` | Function/method has a return section in docstring, but there are no return statements or annotations |
| `DOC203` | Return type(s) in the docstring not consistent with the return annotation                            |

Note on `DOC201`: Methods with `@property` as its last decorator do not need to
have a return section.

### 3.3. `DOC3xx`: Violations about class docstring and class constructor

| Code     | Explanation                                                                                             |
| -------- | ------------------------------------------------------------------------------------------------------- |
| `DOC301` | `__init__()` should not have a docstring; please combine it with the docstring of the class             |
| `DOC302` | The class docstring does not need a "Returns" section, because `__init__()` cannot return anything      |
| `DOC303` | The `__init__()` docstring does not need a "Returns" section, because it cannot return anything         |
| `DOC304` | Class docstring has an argument/parameter section; please put it in the `__init__()` docstring          |
| `DOC305` | Class docstring has a "Raises" section; please put it in the `__init__()` docstring                     |
| `DOC306` | The class docstring does not need a "Yields" section, because `__init__()` cannot yield anything        |
| `DOC307` | The `__init__()` docstring does not need a "Yields" section, because `__init__()` cannot yield anything |

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

## 4. Additional notes

If you'd like to use _pydoclint_ for your project, it is recommended that you
read these additional notes
[here](https://jsh9.github.io/pydoclint/addl_notes.html).
