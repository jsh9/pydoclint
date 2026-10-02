# Configuration options of _pydoclint_

There are many configuration options available. They can be used invidually or
together.

For how to actually implement these options in your commands, please read this
page:
[How to configure _pydoclint_](https://jsh9.github.io/pydoclint/how_to_config.html).

<!--TOC-->

______________________________________________________________________

**Table of Contents**

- [1. `--quiet` (shortform: `-q`)](#1---quiet-shortform--q)
- [2. `--exclude`](#2---exclude)
- [3. `--style`](#3---style)
- [4. `--arg-type-hints-in-docstring` and `--arg-type-hints-in-signature`](#4---arg-type-hints-in-docstring-and---arg-type-hints-in-signature)
- [5. `--check-arg-order` (shortform: `-ao`, default: `True`)](#5---check-arg-order-shortform--ao-default-true)
- [6. `--skip-checking-short-docstrings` (shortform: `-scsd`, default: `True`)](#6---skip-checking-short-docstrings-shortform--scsd-default-true)
- [7. `--skip-checking-raises` (shortform: `-scr`, default: `False`)](#7---skip-checking-raises-shortform--scr-default-false)
- [8. `--skip-checking-private-functions` (shortform: `-scpf`, default: `False`)](#8---skip-checking-private-functions-shortform--scpf-default-false)
- [9. `--allow-init-docstring` (shortform: `-aid`, default: `False`)](#9---allow-init-docstring-shortform--aid-default-false)
- [10. `--require-return-section-when-returning-nothing` (shortform: `-rrs`, default: `False`)](#10---require-return-section-when-returning-nothing-shortform--rrs-default-false)
- [11. `--check-return-types` (shortform: `-crt`, default: `True`)](#11---check-return-types-shortform--crt-default-true)
- [12. `--require-yield-section-when-yielding-nothing` (shortform: `-rys`, default: `True`)](#12---require-yield-section-when-yielding-nothing-shortform--rys-default-true)
- [13. `--check-yield-types` (shortform: `-cyt`, default: `True`)](#13---check-yield-types-shortform--cyt-default-true)
- [14. `--ignore-underscore-only-args` (shortform: `-iuoa`, default: `True`)](#14---ignore-underscore-only-args-shortform--iuoa-default-true)
- [15. `--ignore-private-args` (shortform: `-ipa`, default: `False`)](#15---ignore-private-args-shortform--ipa-default-false)
- [16. `--ignore-special-dunder-args` (shortform: `-isda`, default: `False`)](#16---ignore-special-dunder-args-shortform--isda-default-false)
- [17. `--check-class-attributes` (shortform: `-cca`, default: `True`)](#17---check-class-attributes-shortform--cca-default-true)
- [18. `--ignore-private-class-attributes` (shortform: `-ipca`, default: `True`)](#18---ignore-private-class-attributes-shortform--ipca-default-true)
- [19. `--ignore-underscore-only-class-attributes` (shortform: `-iuoca`, default: `True`)](#19---ignore-underscore-only-class-attributes-shortform--iuoca-default-true)
- [20. `--ignore-special-dunder-class-attributes` (shortform: `-isdca`, default: `True`)](#20---ignore-special-dunder-class-attributes-shortform--isdca-default-true)
- [21. `--treat-property-methods-as-class-attributes` (shortform: `-tpmaca`, default: `False`)](#21---treat-property-methods-as-class-attributes-shortform--tpmaca-default-false)
- [22. `--only-attrs-with-ClassVar-are-treated-as-class-attrs` (shortform: `-oawcv`, default: `False`)](#22---only-attrs-with-classvar-are-treated-as-class-attrs-shortform--oawcv-default-false)
- [23. `--require-inline-class-var-docs` (shortform: `-ricvd`, default: `False`)](#23---require-inline-class-var-docs-shortform--ricvd-default-false)
- [24. `--should-document-star-arguments` (shortform: `-sdsa`, default: `True`)](#24---should-document-star-arguments-shortform--sdsa-default-true)
- [25. `--omit-stars-when-documenting-varargs` (shortform: `-oswdv`, default: `False`)](#25---omit-stars-when-documenting-varargs-shortform--oswdv-default-false)
- [26. `--check-style-mismatch` (shortform: `-csm`, default: `False`)](#26---check-style-mismatch-shortform--csm-default-false)
- [27. `--check-arg-defaults` (shortform: `-cad`, default: `False`)](#27---check-arg-defaults-shortform--cad-default-false)
- [28. `--baseline`](#28---baseline)
- [29. `--generate-baseline` (default: `False`)](#29---generate-baseline-default-false)
- [30. `--auto-regenerate-baseline` (shortform: `-arb`, default: `True`)](#30---auto-regenerate-baseline-shortform--arb-default-true)
- [31. `--show-filenames-in-every-violation-message` (shortform: `-sfn`, default: `False`)](#31---show-filenames-in-every-violation-message-shortform--sfn-default-false)
- [32. `--native-mode-noqa-location` (shortform: `-nmnl`, default: `docstring`)](#32---native-mode-noqa-location-shortform--nmnl-default-docstring)
- [33. `--include-stub-files` (shortform: `-isf`, default: `False`)](#33---include-stub-files-shortform--isf-default-false)
- [34. `--config` (default: `pyproject.toml`)](#34---config-default-pyprojecttoml)

______________________________________________________________________

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

Which style of docstring is your code base using. Right now there are three
available choices: `numpy`, `google`, and `sphinx`. The default value is
`numpy`.

```
pydoclint --style=google <FILE_OR_FOLDER>
```

or

```
flake8 --style=google <FILE_OR_FOLDER>
```

## 4. `--arg-type-hints-in-docstring` and `--arg-type-hints-in-signature`

- `--arg-type-hints-in-docstring`
  - Shortform: `-athd`
  - Default: `True`
  - Meaning:
    - If `True`, there need to be type hints in the argument list of a
      docstring
    - If `False`, there cannot be any type hints in the argument list of a
      docstring
- `--arg-type-hints-in-signature`
  - Shortform: `-aths`
  - Default: `True`
  - Meaning:
    - If `True`, there need to be type hints for input arguments in the
      function/method signature
    - If `False`, there cannot be any type hints for input arguments in the
      function/method signature

Note: if users choose `True` for both options, the argument type hints in the
signature and in the docstring need to match, otherwise there will be a style
violation.

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

## 8. `--skip-checking-private-functions` (shortform: `-scpf`, default: `False`)

If `True`, _pydoclint_ won't check private functions (such as `_helper` and
`__name_mangled`) or underscore-only functions (such as `_` and `__`). Special
dunder methods (such as `__init__`) are still checked. Any functions defined
within skipped functions are also skipped. See
[names with leading underscores](https://jsh9.github.io/pydoclint/leading_underscore_names.html)
for how names are classified.

## 9. `--allow-init-docstring` (shortform: `-aid`, default: `False`)

If it is set to `True`, having a docstring for class constructors
(`__init__()`) is allowed, and the arguments are expected to be documented
under `__init__()` rather than in the class docstring.

Note: the default is set to `False` because not every class has an `__init__`
method (such as classes that inherit from parent classes), but every class must
have the `class ClassName` declaration.

## 10. `--require-return-section-when-returning-nothing` (shortform: `-rrs`, default: `False`)

If `False`, a "return" section is not necessary in the docstring if the
function implicitly returns `None` (for example, doesn't have a return
statement, or has `-> None` as the return annotation) or doesn't return at all
(has return type `NoReturn`).

## 11. `--check-return-types` (shortform: `-crt`, default: `True`)

If True, check that the type(s) in the docstring return section and the return
annotation in the function signature are consistent

## 12. `--require-yield-section-when-yielding-nothing` (shortform: `-rys`, default: `True`)

If False, a yields section is not needed in docstring if the function yields
None.

## 13. `--check-yield-types` (shortform: `-cyt`, default: `True`)

If True, check that the type(s) in the docstring "yields" section and the
return annotation in the function signature are consistent.

## 14. `--ignore-underscore-only-args` (shortform: `-iuoa`, default: `True`)

If True, arguments whose names contain only underscores (such as `_`, `__`,
`*_`, and `**__`) are excluded and must not appear in the docstring. The
leading `*` or `**` of a star argument is removed before its name is
classified.

Private arguments such as `_a` are not underscore-only arguments; they are
controlled by `--ignore-private-args`. See
[names with leading underscores](https://jsh9.github.io/pydoclint/leading_underscore_names.html).

**Why the default is `True`:** a name made only of underscores (`_`, `__`,
`*_`, `**__`) marks an argument that is intentionally unused, such as a
callback parameter that the function must accept but ignores. There is nothing
to document about it. This is also the default of the removed
`--ignore-underscore-args` option, so existing projects keep their behavior.

The removed `--ignore-underscore-args` option now stops the lint run with a
migration error. Delete the old setting when it is `true`, because that is the
new default. When it is `false`, replace it with one of these equivalent forms:

```console
pydoclint --ignore-underscore-only-args=False .
```

```toml
ignore-underscore-only-args = false
```

## 15. `--ignore-private-args` (shortform: `-ipa`, default: `False`)

If True, private arguments (such as `_value`, `__value`, and `*_args`) are
excluded and must not appear in the docstring. Underscore-only arguments (such
as `_`) are controlled by `--ignore-underscore-only-args`, and special dunder
arguments (such as `__value__`) by `--ignore-special-dunder-args`. See
[names with leading underscores](https://jsh9.github.io/pydoclint/leading_underscore_names.html).

**Why the default is `False`:** an underscore prefix doesn't take an argument
out of the call signature; callers can still pass it, so it is documented and
checked like any other argument. Set this option to `True` if your private
arguments are reserved for internal callers, such as recursion state or test
hooks, and you don't want to document them.

## 16. `--ignore-special-dunder-args` (shortform: `-isda`, default: `False`)

If True, special dunder arguments, whose names start and end with double
underscores (such as `__value__` and `**__value__`), are excluded and must not
appear in the docstring. The leading `*` or `**` of a star argument is removed
before its name is classified. See
[names with leading underscores](https://jsh9.github.io/pydoclint/leading_underscore_names.html).

**Why the default is `False`:** like a private argument, a special dunder
argument is part of the call signature, so it is documented and checked by
default. Such argument names are rare. With this default, the default
configuration treats them exactly as it did before this option existed.

Before this option existed, `--ignore-private-args` also controlled special
dunder arguments. If you set `--ignore-private-args=True` and want dunder
arguments to stay ignored, also set `--ignore-special-dunder-args=True`.

## 17. `--check-class-attributes` (shortform: `-cca`, default: `True`)

If True, check the class attributes (defined under the class definition)
against the "Attributes" section of the class's docstring.

Please read
[this page](https://jsh9.github.io/pydoclint/checking_class_attributes.html)
for more instructions.

## 18. `--ignore-private-class-attributes` (shortform: `-ipca`, default: `True`)

If True, private class attributes (underscore-prefixed names containing at
least one non-underscore character, excluding special names that start and end
with double underscores) are excluded and must not appear in the docstring. If
False, they must be documented. See
[names with leading underscores](https://jsh9.github.io/pydoclint/leading_underscore_names.html).

**Why the default is `True`:** the class docstring's "Attributes" section
describes the class's public interface. Private class attributes, such as
`_cache` or `_registry`, are implementation details that users of the class
shouldn't rely on, so they are left out by default. This matches the default of
the removed `--should-document-private-class-attributes` option (`False`).

## 19. `--ignore-underscore-only-class-attributes` (shortform: `-iuoca`, default: `True`)

If True, class attributes whose names contain only underscores (such as `_`,
`__`, ...) are excluded and must not appear in the docstring. If False, they
must be documented. See
[names with leading underscores](https://jsh9.github.io/pydoclint/leading_underscore_names.html).

**Why the default is `True`:** a class attribute named only with underscores is
a placeholder, not data. For example, `_: dataclasses.KW_ONLY` is a dataclass
marker that makes the fields after it keyword-only; it isn't an attribute of
the instances. There is nothing to document, so it is ignored by default. This
matches the default of the removed `--should-document-private-class-attributes`
option (`False`).

To require documentation for `_value` while ignoring placeholders such as `_`
(for example, `_: dataclasses.KW_ONLY`), use:

```toml
ignore-private-class-attributes = false
ignore-underscore-only-class-attributes = true
```

## 20. `--ignore-special-dunder-class-attributes` (shortform: `-isdca`, default: `True`)

If True, special class attributes whose names start and end with double
underscores (such as `__slots__`, `__match_args__`, and `__tablename__`) are
excluded and must not appear in the docstring. If False, they must be
documented. See
[names with leading underscores](https://jsh9.github.io/pydoclint/leading_underscore_names.html).

**Why the default is `True`:** special dunder class attributes, such as
`__slots__`, `__match_args__`, `__hash__ = None`, or SQLAlchemy's
`__tablename__`, configure how Python or a framework treats the class. They are
not attributes that users of the class read or set, so they are left out of the
"Attributes" section by default. Set this option to `False` if your project
documents them. This matches the default of the removed
`--should-document-private-class-attributes` option (`False`).

The removed `--should-document-private-class-attributes` option now stops the
lint run with a migration error. Delete the old setting when it is `false`,
because all three replacements default to `true`. When it is `true`, set all
three replacement options to the inverse value, which keeps private,
underscore-only, and special dunder attributes documented:

```console
pydoclint --ignore-private-class-attributes=False \
    --ignore-underscore-only-class-attributes=False \
    --ignore-special-dunder-class-attributes=False .
```

```toml
# Replaces should-document-private-class-attributes = true
ignore-private-class-attributes = false
ignore-underscore-only-class-attributes = false
ignore-special-dunder-class-attributes = false
```

## 21. `--treat-property-methods-as-class-attributes` (shortform: `-tpmaca`, default: `False`)

If True, treat `@property` methods as class properties. This means that they
need to be documented in the "Attributes" section of the class docstring, and
there cannot be any docstring under the @property methods. This option is only
effective when --check-class-attributes is True.

## 22. `--only-attrs-with-ClassVar-are-treated-as-class-attrs` (shortform: `-oawcv`, default: `False`)

If True, only the attributes whose type annotations are wrapped within
`ClassVar` (where `ClassVar` is imported from `typing`) are treated as class
attributes, and all other attributes are treated as instance attributes.

## 23. `--require-inline-class-var-docs` (shortform: `-ricvd`, default: `False`)

If True, class attributes (a.k.a.,
[`ClassVar`](https://typing.python.org/en/latest/spec/class-compat.html#classvar))
must be documented inline. For example:

```python
class MyClass:
    """My class."""

    field1: int = 5
    """int: Field 1 documentation."""
```

If False, class attributes should be documented in the class docstring instead,
and inline attribute docstrings will trigger `DOC606`.

If True, class-level documentation of class attributes will not be allowed, and
an "Attributes" section in the class docstring will trigger `DOC607`.

Inline docstrings may specify the attribute type as the first token in the
docstring followed by a `:`.

## 24. `--should-document-star-arguments` (shortform: `-sdsa`, default: `True`)

If True, "star arguments" (such as `*args`, `**kwargs`, `**props`, etc.) in the
function signature should be documented in the docstring. If False, they should
not appear in the docstring.

## 25. `--omit-stars-when-documenting-varargs` (shortform: `-oswdv`, default: `False`)

If True, docstring argument entries describing `*args` or `**kwargs` may omit
the leading `*`, and pydoclint will still match them against the function
signature. Leave this disabled to require docstrings to include the leading `*`
characters for varargs.

## 26. `--check-style-mismatch` (shortform: `-csm`, default: `False`)

If True, check that style specified in --style matches the detected style of
the docstring. If there is a mismatch, `DOC003` will be reported. Setting this
to False will silence all `DOC003` violations.

Read more about this config option and `DOC003` at
[https://jsh9.github.io/pydoclint/style_mismatch.html](https://jsh9.github.io/pydoclint/style_mismatch.html).

## 27. `--check-arg-defaults` (shortform: `-cad`, default: `False`)

If True, docstring type hints should contain default values consistent with the
function signature. If False, docstring type hints should not contain default
values. (Only applies to numpy and Google styles; not compatible with Sphinx
style.)

In stub (`.pyi`) files, a default of `...` is a placeholder that doesn't say
what the default value is. So an argument or class attribute with that default
can be documented with any default value (such as `int, default=3`) or with no
default (such as `int`). Its type is still checked.

<a id="baseline"></a>

## 28. `--baseline`

Baseline allows you to remember the current project state and then show only
new violations, ignoring old ones. This can be very useful when you'd like to
gradually adopt _pydoclint_ in existing projects.

If you'd like to use this feature, pass in the full file path to this option.
For convenience, you can write this option in your `pyproject.toml` file:

```toml
[tool.pydoclint]
baseline = "pydoclint-baseline.txt"
```

If you also set `--generate-baseline=True` (or `--generate-baseline True`),
_pydoclint_ will generate a file that contains all current violations of your
project.

If `--generate-baseline` is not passed to _pydoclint_ (the default is `False`),
_pydoclint_ will read your baseline file, and ignore all violations specified
in that file.

## 29. `--generate-baseline` (default: `False`)

Required to use with `--baseline` option. If `True`, generate the baseline file
that contains all current violations.

## 30. `--auto-regenerate-baseline` (shortform: `-arb`, default: `True`)

If it's set to True, _pydoclint_ will automatically regenerate the baseline
file every time you fix violations in the baseline and rerun _pydoclint_.

This saves you from having to manually regenerate the baseline file by setting
`--generate-baseline=True` and run _pydoclint_.

## 31. `--show-filenames-in-every-violation-message` (shortform: `-sfn`, default: `False`)

If False, in the terminal the violation messages are grouped by file names:

```
file_01.py
    10: DOC101: ...
    25: DOC105: ...
    37: DOC203: ...

file_02.py
    24: DOC102: ...
    51: DOC107: ...
    126: DOC203: ...
    246: DOC105: ...
```

If True, the file names are printed in the front of every violation message:

```
file_01.py:10: DOC101: ...
file_01.py:25: DOC105: ...
file_01.py:37: DOC203: ...

file_02.py:24: DOC102: ...
file_02.py:51: DOC107: ...
file_02.py:126: DOC203: ...
file_02.py:246: DOC105: ...
```

This can be convenient if you would like to click on each violation message and
go to the corresponding line in your IDE. (Note: not all terminal app offers
this functionality.)

## 32. `--native-mode-noqa-location` (shortform: `-nmnl`, default: `docstring`)

This option controls where _pydoclint_ looks for inline `# noqa: DOCxxx`
comments when running in native mode (i.e., outside of Flake8). Two values are
accepted:

- `docstring` (default): expects the `# noqa: DOCxxx` comment on the same line
  as the closing triple quotes of the docstring.
- `definition`: expects the `# noqa: DOCxxx` comment on the line containing the
  function/method/class definition.

Only DOC-prefixed violation codes are honored; other codes are ignored by the
native parser. This setting has no effect in Flake8 mode, which is controlled
by Flake8's own `noqa` handling.

## 33. `--include-stub-files` (shortform: `-isf`, default: `False`)

If True, _pydoclint_ also checks stub (`.pyi`) files when it scans folders. If
False, it only checks `.py` files in folders. Stub files that you pass in
explicitly are always checked, whatever this option is set to.

```
pydoclint --include-stub-files=True <FOLDER_NAME>
```

The body of a function in a stub file is a placeholder (usually `...`), so
_pydoclint_ doesn't rely on it when it checks functions in stub files:

- `DOC502` isn't reported, because a body without `raise` statements doesn't
  mean that the function doesn't raise anything.
- `DOC202` isn't reported, because a body without `return` statements doesn't
  mean that the function returns nothing. (`DOC203` still reports a "Returns"
  section without a return annotation.)
- `DOC403` is only reported when the return annotation isn't a `Generator`,
  `Iterator`, or `Iterable` (or is missing), because then the function can't
  yield anything. A body without `yield` statements doesn't count.
- A function with an `Iterator` or `Iterable` return annotation can have a
  "Yields" section instead of a "Returns" section (no `DOC201`), because the
  body doesn't show whether it yields or returns an iterator.
- With a `Generator[YieldType, SendType, ReturnType]` return annotation, the
  "Returns" section can document either `ReturnType` (as for a generator that
  both yields and returns) or the whole annotation (as for one that only
  yields).
- `DOC402` and `DOC404` aren't reported, because these checks only run when
  there are `yield` statements in the body (see
  [issue 309](https://github.com/jsh9/pydoclint/issues/309)).

Abstract methods are checked the same way, except that they don't get `DOC403`
at all. The other checks work as usual. This applies whenever a `.pyi` file is
checked, including in _flake8_.

This option is only available in the native command-line mode. If you use
_pydoclint_ within _flake8_, you can use _flake8_'s
[`--filename` option](https://flake8.pycqa.org/en/latest/user/options.html#cmdoption-flake8-filename)
instead (for example, `--filename=*.py,*.pyi`).

If you use the `pydoclint` or `pydoclint-flake8` pre-commit hook, pre-commit
doesn't pass stub files to it by default. To check them, override the hook's
file types in your `.pre-commit-config.yaml` (you don't need
`--include-stub-files` here, because pre-commit passes files in explicitly):

```yaml
- repo: https://github.com/jsh9/pydoclint
  rev: <latest_tag>
  hooks:
    - id: pydoclint  # or pydoclint-flake8
      types: [file]
      types_or: [python, pyi]
```

## 34. `--config` (default: `pyproject.toml`)

The full path of the .toml config file that contains the config options. Note
that the command line options take precedence over the .toml file. Look at this
page:
[How to configure _pydoclint_](https://jsh9.github.io/pydoclint/how_to_config.html)
