# How to ignore certain violations

<!--TOC-->

______________________________________________________________________

**Table of Contents**

- [1. As a native tool](#1-as-a-native-tool)
- [2. As a _flake8_ plugin](#2-as-a-flake8-plugin)
  - [2.1. Usage with Ruff](#21-usage-with-ruff)

______________________________________________________________________

<!--TOC-->

## 1. As a native tool

You can suppress `DOC` violations inline with the same `# noqa:` syntax that
_flake8_ and Ruff understand. When running the native CLI, set where those
comments live with `--native-mode-noqa-location` (`docstring` by default, also
accepts `definition`):

- `docstring`: put the `# noqa:` comment after the closing triple quotes of the
  docstring.
- `definition`: put the comment on the line that defines the function/class.

```python
def funcDocstringComment(arg1: int, arg2: int) -> None:
    """Docstring text.
    """  # noqa: DOC101, DOC103


def funcDefinitionComment(arg1: int, arg2: int) -> None:  # noqa: DOC103
    """Docstring text."""
```

Multiple DOC codes can be listed, and partial prefixes work as well. For
example, `# noqa: DOC1` suppresses every violation whose code starts with
`DOC1` (e.g., `DOC101`, `DOC103`).

## 2. As a _flake8_ plugin

In _flake8_ mode (meaning that you use _pydoclint_ as a flake8 plugin), if
you'd like to ignore a specific violation code (such as `DOC201` and `DOC301`)
in-line, you can add this comment to the function of your choice:

```python
def my_function(  # noqa: DOC201, DOC301
        arg1,
        arg2,
) -> None:
    ...
```

If you would like to ignore certain categories of violations (such as `DOC2xx`)
in-line, you can do this:

```python
def my_function(  # noqa: DOC2
        arg1,
        arg2,
) -> None:
    ...
```

All the usage is consistent with how you would use _flake8_. Please read the
official _flake8_ documentation for full details:
https://flake8.pycqa.org/en/latest/user/violations.html.

### 2.1. Usage with [Ruff](https://github.com/astral-sh/ruff)

With `ruff>=0.1.3`, allowlist `DOC` codes using the
[`external` setting](https://docs.astral.sh/ruff/settings/#external):

Put the following in your `pyproject.toml` file:

```toml
[tool.ruff]
external = [
    "DOC",  # pydoclint
]
```
