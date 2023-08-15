# How to ignore certain violations in *flake8* mode

In *flake8* mode (meaning that you use *pydoclint* as a flake8 plugin), if you'd like to ignore a specific violation code (such as `DOC201` and `DOC301`) in-line, you can add this comment to the function of your choice:

```python
def my_function(  # noqa: DOC201, DOC301
        arg1,
        arg2,
) -> None:
    ...
```

If you would like to ignore certain categories of violations (such as `DOC2xx`) in-line, you can do this:

```python
def my_function(  # noqa: DOC2
        arg1,
        arg2,
) -> None:
    ...
```

All the usage is consistent with how you would use *flake8*.  Please read the official *flake8* documentation for full details: https://flake8.pycqa.org/en/latest/user/violations.html.
