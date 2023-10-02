# Configuration options of _pydoclint_

There are several configuration options available. They can be used invidually
or together.

For how to actually implement these options in your commands, please read this
page:
[How to configure _pydoclint_](https://jsh9.github.io/pydoclint/how_to_config.html).

**Table of Contents**

<!--TOC-->

- [1. `--quiet` (shortform: `-q`)](#1---quiet-shortform--q)
- [2. `--exclude`](#2---exclude)
- [3. `--style`](#3---style)
- [4. `--type-hints-in-docstring` and `--type-hints-in-signature`](#4---type-hints-in-docstring-and---type-hints-in-signature)
- [5. `--check-arg-order` (shortform: `-ao`, default: `True`)](#5---check-arg-order-shortform--ao-default-true)
- [6. `--skip-checking-short-docstrings` (shortform: `-scsd`, default: `True`)](#6---skip-checking-short-docstrings-shortform--scsd-default-true)
- [7. `--skip-checking-raises` (shortform: `-scr`, default: `False`)](#7---skip-checking-raises-shortform--scr-default-false)
- [8. `--allow-init-docstring` (shortform: `-aid`, default: `False`)](#8---allow-init-docstring-shortform--aid-default-false)
- [9. `--require-return-section-when-returning-nothing` (shortform: `-rrs`, default: `False`)](#9---require-return-section-when-returning-nothing-shortform--rrs-default-false)
- [10. `--check-return-types` (shortform: `-crt`, default: `True`)](#10---check-return-types-shortform--crt-default-true)
- [11. `--check-yield-types` (shortform: `-cyt`, default: `True`)](#11---check-yield-types-shortform--cyt-default-true)
- [12. `--baseline`](#12---baseline)
- [13. `--generate-baseline` (default: `False`)](#13---generate-baseline-default-false)
- [14. `--config` (default: `pyproject.toml`)](#14---config-default-pyprojecttoml)

<!--TOC-->

## 1. `--quiet` (shortform: `-q`)

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

## 2. `--exclude`

You can use this option to exclude files within the given folder. It is a regex
pattern of full file paths.

For example:

```
pydoclint --exclude='\.git|\.tox|tests/data' <FOLDER_NAME>
```

This option is only available in the native command-line mode. If you use
_pydoclint_ within _flake8_, you can use _flake8_'s
[`--exclude` option](https://flake8.pycqa.org/en/latest/user/options.html#cmdoption-flake8-exclude).

## 3. `--style`

Which style of docstring is your code base using. Right now there are two
available choices: `numpy` and `google`. The default value is `numpy`.

```
pydoclint --style=google <FILE_OR_FOLDER>
```

or

```
flake8 --style=google <FILE_OR_FOLDER>
```

## 4. `--type-hints-in-docstring` and `--type-hints-in-signature`

- `--type-hints-in-docstring`
  - Shortform: `-thd`
  - Default: `True`
  - Meaning:
    - If `True`, there need to be type hints in the argument list of a
      docstring
    - If `False`, there cannot be any type hints in the argument list of a
      docstring
- `--type-hints-in-signature`
  - Shortform: `-ths`
  - Default: `True`
  - Meaning:
    - If `True`, there need to be type hints in the function/method signature
    - If `False`, there cannot be any type hints in the function/method
      signature

Note: if users choose `True` for both options, the type hints in the signature
and in the docstring need to match, otherwise there will be a style violation.

## 5. `--check-arg-order` (shortform: `-ao`, default: `True`)

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

## 6. `--skip-checking-short-docstrings` (shortform: `-scsd`, default: `True`)

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

## 7. `--skip-checking-raises` (shortform: `-scr`, default: `False`)

If `True`, _pydoclint_ won't report `DOC501` or `DOC502` if there are `raise`
statements in the function/method but there aren't any "raises" sections in the
docstring (or vice versa).

## 8. `--allow-init-docstring` (shortform: `-aid`, default: `False`)

If it is set to `True`, having a docstring for class constructors
(`__init__()`) is allowed, and the arguments are expected to be documented
under `__init__()` rather than in the class docstring.

## 9. `--require-return-section-when-returning-nothing` (shortform: `-rrs`, default: `False`)

If `False`, a "return" section is not necessary in the docstring if the
function implicitly returns `None` (for example, doesn't have a return
statement, or has `-> None` as the return annotation) or doesn't return at all
(has return type `NoReturn`).

## 10. `--check-return-types` (shortform: `-crt`, default: `True`)

If True, check that the type(s) in the docstring return section and the return
annotation in the function signature are consistent

## 11. `--check-yield-types` (shortform: `-cyt`, default: `True`)

If True, check that the type(s) in the docstring "yields" section and the
return annotation in the function signature are consistent.

## 12. `--baseline`

Baseline allows you to remember the current project state and then show only
new errors, ignoring old ones.

The path to the file is expected. It is recommended to add this option to
config file. (Default is `pyproject.toml`)

```toml
[tool.pydoclint]
baseline = "pydoclint-baseline.txt"
```

if `--generate-baseline True` is passed, then pydoclint generate file, that
contains all current errors of project. If `--generate-baseline` is not passed
(default value is `False`) then pydoclint will read your baseline file, and
ignore all errors, specified in that file.

## 13. `--generate-baseline` (default: `False`)

Required to use with `--baseline` option. If `True`, generate file, that
contains all current errors of project.

## 14. `--config` (default: `pyproject.toml`)

The full path of the .toml config file that contains the config options. Note
that the command line options take precedence over the .toml file. Look at this
page:
[How to configure _pydoclint_](https://jsh9.github.io/pydoclint/how_to_config.html)
