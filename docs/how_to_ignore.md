# How to ignore certain violations in _flake8_ mode

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
