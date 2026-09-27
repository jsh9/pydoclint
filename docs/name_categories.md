# Name categories

<!--TOC-->

______________________________________________________________________

**Table of Contents**

- [1. Categories](#1-categories)
- [2. Which options apply to which categories](#2-which-options-apply-to-which-categories)
- [3. Default values](#3-default-values)
- [4. Ignored names are not optional](#4-ignored-names-are-not-optional)

______________________________________________________________________

<!--TOC-->

## 1. Categories

_pydoclint_ puts every function, argument, and class attribute name into
exactly one category:

| Category          | Examples                                 |
| ----------------- | ---------------------------------------- |
| `PUBLIC`          | `value`, `value_`                        |
| `PRIVATE`         | `_value`, `__value`, `_value__`          |
| `UNDERSCORE_ONLY` | `_`, `__`, `___`                         |
| `SPECIAL_DUNDER`  | `__init__`, `__slots__`, `__tablename__` |

## 2. Which options apply to which categories

| Option                                      | Applies to                                |
| ------------------------------------------- | ----------------------------------------- |
| `--skip-checking-private-functions`         | `PRIVATE` and `UNDERSCORE_ONLY` functions |
| `--ignore-private-args`                     | `PRIVATE` arguments                       |
| `--ignore-underscore-only-args`             | `UNDERSCORE_ONLY` arguments               |
| `--ignore-special-dunder-args`              | `SPECIAL_DUNDER` arguments                |
| `--ignore-private-class-attributes`         | `PRIVATE` class attributes                |
| `--ignore-underscore-only-class-attributes` | `UNDERSCORE_ONLY` class attributes        |
| `--ignore-special-dunder-class-attributes`  | `SPECIAL_DUNDER` class attributes         |

In particular:

- `--skip-checking-private-functions` skips private and underscore-only
  functions, together with everything defined inside them. Special dunder
  methods, such as `__init__`, are always checked.
- Arguments and class attributes each have three options that independently
  control private, underscore-only, and special dunder names.
- The leading `*` or `**` of a star argument is removed before its name is
  classified, so `*_` is underscore-only and `**_kwargs` is private.
- Public names are never ignored by these options.

## 3. Default values

The defaults follow one rule per context. Arguments are part of a function's
call signature, so only underscore-only placeholder arguments are ignored by
default. The "Attributes" section describes a class's public interface, so
private, underscore-only, and special dunder class attributes are all ignored
by default. Each option's section in
[Configuration options](https://jsh9.github.io/pydoclint/config_options.html)
explains its default in more detail.

## 4. Ignored names are not optional

An ignored argument or class attribute is excluded from comparison; it is not
optional documentation. Documenting an ignored name produces an "extra name"
violation, such as `DOC102`/`DOC103` for arguments or `DOC602`/`DOC603` for
class attributes.
