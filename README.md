# pydoclint

A Python docstring linter to check whether a docstring's sections (arguments,
returns, raises, ...) match the function signature or function implementation.

It runs really fast. In fact, it is at least ~1,475 times faster than
[darglint](https://github.com/terrencepreilly/darglint) (another linter of the
same purposes which is no longer maintained).

Here is a comparison of linting time on some famous Python projects:

|                                                              | pydoclint | darglint                          |
| ------------------------------------------------------------ | --------- | --------------------------------- |
| [numpy](https://github.com/numpy/numpy)                      | 2.0 sec   | 49 min 9 sec (1,475x slower)      |
| [scikit-learn](https://github.com/scikit-learn/scikit-learn) | 2.4 sec   | 3 hr 5 min 33 sec (4,639x slower) |

Currently, _pydoclint_ supports two docstring styles:

- The [numpy stlyle](https://numpydoc.readthedocs.io/en/latest/format.html)
- The
  [Google style](https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html)

Support for the
[Sphinx style](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html)
may be added in the future if there are requests for it.

Another note: this linter and [pydocstyle](https://github.com/PyCQA/pydocstyle)
serves complementary purposes. It is recommended that you use both together.

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

### 2.3. Native vs _flake8_

Should I use _pydoclint_ as a native command line tool or a _flake8_ plugin?
Here's comparison:

|                 | Pros                                     | Cons                                                          |
| --------------- | ---------------------------------------- | ------------------------------------------------------------- |
| Native tool     | Slightly faster                          | No inline or project-wide omission support right now [*]      |
| _flake8_ plugin | Supports inline or project-wide omission | Slightly slower because other flake8 plugins are run together |

\*) This feature may be added in the near future

### 2.4. Configuration

Here is how to configure _pydoclint_. For detailed explanations of all options,
see [Section 4](#4-configuration-options) below.

#### 2.4.1. Setting options inline

- Native:

  ```bash
  pydoclint --check-arg-order=False <FILE_OR_FOLDER_PATH>
  ```

- Flake8:

  ```bash
  flake8 --check-arg-order=False <FILE_OR_FOLDER_PATH>
  ```

#### 2.4.2. Setting options in a configuration file

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

| Code     | Explanation                                                                                                                                          |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DOC101` | Docstring contains fewer arguments than in function signature                                                                                        |
| `DOC102` | Docstring contains more arguments than in function signature                                                                                         |
| `DOC103` | Docstring arguments are different from function arguments. (Or could be other formatting issues: https://github.com/jsh9/pydoclint/#notes-on-doc103) |
| `DOC104` | Arguments are the same in the docstring and the function signature, but are in a different order.                                                    |
| `DOC105` | Argument names match, but type hints do not match                                                                                                    |

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

## 4. Configuration options

There are several configuration options available. They can be used invidually
or together.

### 4.1. `--quiet` (shortform: `-q`)

This flag activates the "quite mode", in which no output will be printed to the
command line if there are no violations.

By default, this flag is _not_ activated, so the files that are scanned are
printed in the command line.

```
pydoclint --quiet <FILE_OR_FOLDER>
```

This option is only available in the "native" command-line mode, rather than in
flake8. If you use pydoclint in flake8, please use flake8's own verbosity
configuration instead.

### 4.2. `--exclude`

You can use this option to exclude files within the given folder. It is a regex
pattern of full file paths.

For example:

```
pydoclint --exclude='\.git|\.tox|tests/data' <FOLDER_NAME>
```

This option is only available in the native command-line mode. If you use
_pydoclint_ within _flake8_, you can use _flake8_'s
[`--exclude` option](https://flake8.pycqa.org/en/latest/user/options.html#cmdoption-flake8-exclude).

### 4.3. `--style`

Which style of docstring is your code base using. Right now there are two
available choices: `numpy` and `google`. The default value is `numpy`.

```
pydoclint --style=google <FILE_OR_FOLDER>
```

or

```
flake8 --style=google <FILE_OR_FOLDER>
```

### 4.4. `--check-type-hint` (shortform: `-th`, default: `True`)

If `True`, the type hints in the docstring and in the Python code need to
exactly match.

To turn this option on/off, do this:

```
pydoclint --check-type-hint=False <FILE_OR_FOLDER>
```

or

```
flake8 --check-type-hint=False <FILE_OR_FOLDER>
```

### 4.5. `--check-arg-order` (shortform: `-ao`, default: `True`)

If `True`, the input argument order in the docstring needs to match that in the
function signature.

To turn this option on/off, do this:

```
pydoclint --check-arg-order=False <FILE_OR_FOLDER>
```

or

```
flake8 --check-arg-order=False <FILE_OR_FOLDER>
```

### 4.6. `--skip-checking-short-docstrings` (shortform: `-scsd`, default: `True`)

If `True`, `pydoclint` won't check functions that have only a short description
in their docstring.

To turn this option on/off, do this:

```
pydoclint --skip-checking-short-docstrings=False <FILE_OR_FOLDER>
```

or

```
flake8 --skip-checking-short-docstrings=False <FILE_OR_FOLDER>
```

### 4.7. `--skip-checking-raises` (shortform: `-scr`, default: `False`)

If `True`, _pydoclint_ won't report `DOC501` or `DOC502` if there are `raise`
statements in the function/method but there aren't any "raises" sections in the
docstring (or vice versa).

### 4.8. `--allow-init-docstring` (shortform: `-aid`, default: `False`)

If it is set to `True`, having a docstring for class constructors
(`__init__()`) is allowed, and the arguments are expected to be documented
under `__init__()` rather than in the class docstring.

### 4.9. `--require-return-section-when-returning-none` (shortform: `-rrs`, default: `False`)

If `False`, a "return" section is not necessary in the docstring if the
function implicitly returns `None` (for example, doesn't have a return
statement, or has `-> None` as the return annotation).
