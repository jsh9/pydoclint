# pydoclint

[![Downloads](https://static.pepy.tech/badge/pydoclint)](https://pepy.tech/project/pydoclint)
[![Downloads](https://static.pepy.tech/badge/pydoclint/month)](https://pepy.tech/project/pydoclint)
[![Downloads](https://static.pepy.tech/badge/pydoclint/week)](https://pepy.tech/project/pydoclint)

_pydoclint_ is the go-to linter for making sure Python docstrings match the
code they describe, with
[![](https://static.pepy.tech/personalized-badge/pydoclint?period=monthly&units=international_system&left_text=&left_color=green&right_color=green)](https://pepy.tech/project/pydoclint)
monthly downloads.

It checks arguments, return values, yields, raises, class attributes, and type
hints in [numpy](https://numpydoc.readthedocs.io/en/latest/format.html),
[Google](https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html),
and
[Sphinx](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html)
styles, with a few
[minor deviations](https://jsh9.github.io/pydoclint/style_deviations.html).

Full documentation:
[jsh9.github.io/pydoclint](https://jsh9.github.io/pydoclint).

<!--TOC-->

______________________________________________________________________

**Table of Contents**

- [1. Why _pydoclint_?](#1-why-pydoclint)
  - [1.1. Docstrings that stay true to the code](#11-docstrings-that-stay-true-to-the-code)
  - [1.2. Built for the age of AI-assisted coding](#12-built-for-the-age-of-ai-assisted-coding)
  - [1.3. Highly configurable](#13-highly-configurable)
  - [1.4. _pydoclint_ vs Ruff's `DOC` rules](#14-pydoclint-vs-ruffs-doc-rules)
  - [1.5. How to adopt _pydoclint_?](#15-how-to-adopt-pydoclint)
- [2. Installation](#2-installation)
- [3. Usage](#3-usage)
  - [3.1. As a native command line tool](#31-as-a-native-command-line-tool)
  - [3.2. As a _flake8_ plugin](#32-as-a-flake8-plugin)
  - [3.3. Native vs _flake8_](#33-native-vs-flake8)
  - [3.4. As a pre-commit hook](#34-as-a-pre-commit-hook)
    - [3.4.1. Native mode](#341-native-mode)
    - [3.4.2. As a _flake8_ plugin](#342-as-a-flake8-plugin)
  - [3.5. How to configure _pydoclint_](#35-how-to-configure-pydoclint)
  - [3.6. How to ignore certain violations](#36-how-to-ignore-certain-violations)
  - [3.7. Additional tips, tricks, and pitfalls](#37-additional-tips-tricks-and-pitfalls)
    - [3.7.1. How to _not_ document certain functions?](#371-how-to-not-document-certain-functions)
    - [3.7.2. Pitfall: type hints and default values](#372-pitfall-type-hints-and-default-values)
- [4. Style violation codes](#4-style-violation-codes)
- [5. Documentation map](#5-documentation-map)

______________________________________________________________________

<!--TOC-->

## 1. Why _pydoclint_?

### 1.1. Docstrings that stay true to the code

A docstring that disagrees with its code is worse than none.

_pydoclint_ catches the drift from everyday edits (a renamed argument, a new
`raise`, a changed return type, an undocumented class attribute) and reports
each one as a
[precise violation](https://jsh9.github.io/pydoclint/violation_codes.html).

### 1.2. Built for the age of AI-assisted coding

AI coding agents write "mostly correct" docstrings, but omissions and
hallucinations inevitably happen. That's why a deterministic docstring linter
matters more than ever:

- **Docstrings are context for AI.** A stale docstring misleads the next agent
  that reads it.
- **Reduce AI token usage.** Agents don't need to spend tokens checking
  docstrings by hand; _pydoclint_ does it deterministically.
- **Fast enough for every change.** It takes only 3 seconds, even on huge
  codebases like [numpy](https://github.com/numpy/numpy) (200k+ lines of code,
  1,600+ classes, ~12k functions/methods).
- **Agents can fix what it reports.** Violation messages are specific and
  actionable, so an agent can correct them without a human in the loop.

### 1.3. Highly configurable

_pydoclint_ offers
[30+ configuration options](https://jsh9.github.io/pydoclint/config_options.html)
for you to fine-tune it to fit your team's conventions. It also offers a
"baseline" mode to ease adoption in legacy codebases.

### 1.4. _pydoclint_ vs Ruff's `DOC` rules

[Ruff](https://docs.astral.sh/ruff/rules/#pydoclint-doc) re-implements a small
subset of _pydoclint_'s rules. As of September 2026, Ruff still lacks many of
_pydoclint_'s features:

|                                | _pydoclint_ | Ruff (`DOC` rules) |
| ------------------------------ | ----------- | ------------------ |
| Number of rules                | 39          | 7                  |
| Number of config options       | 30+         | 2                  |
| Checks type hints              | ✅          | ❌                 |
| Checks class attributes        | ✅          | ❌                 |
| Sphinx style support           | ✅          | ❌                 |
| "Baseline" mode                | ✅          | ❌                 |
| Docstring style mismatch check | ✅          | ❌                 |

Therefore, we recommend using _pydoclint_ to check docstrings and letting Ruff
handle other lint rules.

### 1.5. How to adopt _pydoclint_?

If you write code manually, this documentation is a good place to start. If you
use AI assistants to code, simply say:

> Help me adopt pydoclint in my codebase. Read its documentation at
> https://jsh9.github.io/pydoclint

Additionally, it is highly recommended that you also adopt
[_format-docstring_](https://github.com/jsh9/format-docstring) as a pre-commit
hook alongside _pydoclint_. _format-docstring_ syncs argument types, default
values, return types, and class attribute types from your code into your
docstrings, which automatically fixes many (but not all) of the issues that
_pydoclint_ would catch. Run _format-docstring_ first (i.e., list it above
_pydoclint_ in `.pre-commit-config.yaml`), so that _pydoclint_ only reports
what's left to fix. _format-docstring_ also standardizes docstring formatting
to reduce diffs.

Note: _format-docstring_ writes default values into docstrings by default
(e.g., `n : int, default=3`), while _pydoclint_ by default expects docstrings
without them. To make the two tools agree, set _pydoclint_'s
`--check-arg-defaults=True` (or run _format-docstring_ with
`--include-arg-defaults=False`).

Adopting _pydoclint_ in an existing codebase? Use the "baseline" mode: run
_pydoclint_ once with `--baseline=<FILE>` and `--generate-baseline=True` to
record all current violations, and from then on it only reports new ones. With
`--auto-regenerate-baseline` (on by default), the baseline file shrinks as you
fix old violations. See
[the documentation on these options](https://jsh9.github.io/pydoclint/config_options.html#baseline)
for details.

[pydocstyle](https://github.com/PyCQA/pydocstyle) (or the `D` rules in Ruff) is
recommended too, as it checks some style rules that _pydoclint_ isn't designed
to cover.

## 2. Installation

To install only the native _pydoclint_ tooling, run this command:

```
pip install pydoclint
```

To use _pydoclint_ as a _flake8_ plugin, please run this command, which will
also install _flake8_ to the current Python environment:

```
pip install pydoclint[flake8]
```

_pydoclint_ requires Python 3.10 or newer.

## 3. Usage

### 3.1. As a native command line tool

```
pydoclint <FILE_OR_FOLDER>
```

Replace `<FILE_OR_FOLDER>` with the file/folder names you want, such as `.`.

### 3.2. As a _flake8_ plugin

Once you install `pydoclint[flake8]`, you can run:

```
flake8 --select=DOC <FILE_OR_FOLDER>
```

If you don't include `--select=DOC` in your command, _flake8_ will also run
other built-in _flake8_ linters on your code.

### 3.3. Native vs _flake8_

Should you use _pydoclint_ as a native command line tool or a _flake8_ plugin?
Here's a comparison:

|                 | Pros                                                                                         | Cons                                                                   |
| --------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Native tool     | Slightly faster; supports ["baseline"](#15-how-to-adopt-pydoclint); supports inline `# noqa` | No project-wide ignore list for violation codes (inline `# noqa` only) |
| _flake8_ plugin | Supports inline or project-wide omission                                                     | Slightly slower because other flake8 plugins are run together          |

> **Tip:** In native mode you can suppress DOC violations inline with
> `# noqa: DOCxxx`. Use the `--native-mode-noqa-location` option (valid values:
> "docstring" or "definition") to decide whether the comment lives on the
> definition line or at the end of the docstring (after the triple quotes).

### 3.4. As a pre-commit hook

_pydoclint_ can be used as a [pre-commit hook](https://pre-commit.com/), either
in native mode or as a _flake8_ plugin.

To use it, put the following in your `.pre-commit-config.yaml` file:

#### 3.4.1. Native mode

```yaml
- repo: https://github.com/jsh9/pydoclint
  rev: <latest_tag>
  hooks:
    - id: pydoclint
      args: [--style=google, --check-return-types=False]
```

(Replace `<latest_tag>` with the latest release tag in
https://github.com/jsh9/pydoclint/releases)

#### 3.4.2. As a _flake8_ plugin

```yaml
- repo: https://github.com/jsh9/pydoclint
  rev: <latest_tag>
  hooks:
    - id: pydoclint-flake8
      args: [--style=google, --check-return-types=False]
```

### 3.5. How to configure _pydoclint_

Please read
[How to configure _pydoclint_](https://jsh9.github.io/pydoclint/how_to_config.html)
for how to set options (on the command line, in `pyproject.toml`, or in
`.pre-commit-config.yaml`), and
[Configuration options](https://jsh9.github.io/pydoclint/config_options.html)
for the full list.

### 3.6. How to ignore certain violations

Please read this page:
[How to ignore certain violations](https://jsh9.github.io/pydoclint/how_to_ignore.html)

### 3.7. Additional tips, tricks, and pitfalls

#### 3.7.1. How to _not_ document certain functions?

If you don't write any docstring for a function, _pydoclint_ will not check it.

Also, if you write a docstring with only a description (without the argument
section, the return section, etc.), _pydoclint_ will not check this docstring,
because the `--skip-checking-short-docstrings` is `True` by default. (You can
set it to `False`.)

#### 3.7.2. Pitfall: type hints and default values

_pydoclint_ compares type hints in docstrings with those in the function
signature verbatim. For example, if the signature says `int | None`, the
docstring should also say `int | None` (not `Optional[int]` or
`int, optional`).

Default values follow the `--check-arg-defaults` option:

- By default (`False`), leave default values out of docstrings: write
  `n : int`, not `n : int, default=3`.
- If set to `True`, default values are required, in the `default=...` form
  (e.g., `n : int, default=3`), and are checked against the signature. (This
  only applies to numpy and Google styles.)

These are deliberate deviations from the official docstring style guides, for
unambiguity and speed. See
[minor style deviations](https://jsh9.github.io/pydoclint/style_deviations.html)
for the details, and
[notes on writing type hints](https://jsh9.github.io/pydoclint/notes_for_users.html#2-notes-on-writing-type-hints)
for the rationale.

## 4. Style violation codes

_pydoclint_ currently has 7 categories of style violation codes:

- `DOC0xx`: Docstring parsing issues
- `DOC1xx`: Violations about input arguments
- `DOC2xx`: Violations about return argument(s)
- `DOC3xx`: Violations about class docstring and class constructor
- `DOC4xx`: Violations about "yield" statements
- `DOC5xx`: Violations about "raise" and "assert" statements
- `DOC6xx`: Violations about class attributes

For detailed explanations of each violation code, please read this page:
[_pydoclint_ style violation codes](https://jsh9.github.io/pydoclint/violation_codes.html).

## 5. Documentation map

Every page of the [full documentation](https://jsh9.github.io/pydoclint):

**Configuration**

- [How to configure _pydoclint_](https://jsh9.github.io/pydoclint/how_to_config.html):
  setting options on the command line, in `pyproject.toml`, or in
  `.pre-commit-config.yaml`
- [Configuration options](https://jsh9.github.io/pydoclint/config_options.html):
  every option, with its default value
- [How to ignore certain violations](https://jsh9.github.io/pydoclint/how_to_ignore.html):
  inline `# noqa` comments, in native mode, with _flake8_, and with Ruff

**Reference**

- [Style violation codes](https://jsh9.github.io/pydoclint/violation_codes.html):
  what each `DOCxxx` code means
- [Minor style deviations](https://jsh9.github.io/pydoclint/style_deviations.html):
  where _pydoclint_ differs from the numpy, Google, and Sphinx style guides
- [Docstring style mismatch (`DOC003`)](https://jsh9.github.io/pydoclint/style_mismatch.html):
  how _pydoclint_ detects the style of a docstring

**Guides**

- [Checking class attributes](https://jsh9.github.io/pydoclint/checking_class_attributes.html)
- [Names with leading underscores](https://jsh9.github.io/pydoclint/leading_underscore_names.html)
- [`Generator` vs `Iterator` (`DOC405`)](https://jsh9.github.io/pydoclint/notes_generator_vs_iterator.html)

**FAQ and limitations**

- [Notes for users](https://jsh9.github.io/pydoclint/notes_for_users.html):
  cases _pydoclint_ is not designed to handle, notes on type hints, and editor
  integration

**Contributing**

- [Notes for developers](https://jsh9.github.io/pydoclint/notes_for_developers.html):
  if you'd like to contribute to _pydoclint_, thank you! This guide helps you
  get familiar with the code base.
