# Checking class attributes

<!--TOC-->

______________________________________________________________________

**Table of Contents**

- [1. NumPy style](#1-numpy-style)
- [2. Google style](#2-google-style)
- [3. Sphinx style](#3-sphinx-style)
- [4. Special note: inline docstrings](#4-special-note-inline-docstrings)
- [5. Private, underscore-only, and special names](#5-private-underscore-only-and-special-names)

______________________________________________________________________

<!--TOC-->

Class attributes are variables defined directly in a class:

```python
class MyPet:
    name: str
    age_in_months: int
    weight_in_kg: float
    is_very_cute_or_not: bool = True
```

Enable
[`--check-class-attributes`](https://jsh9.github.io/pydoclint/config_options.html)
to compare these attributes with the class docstring.

_pydoclint_ uses the following convention for NumPy, Google, and Sphinx
docstrings:

- Put class attributes in the class docstring's "Attributes" section.
- Put `__init__()` arguments in a separate "Parameters" or "Args" section (or
  use Sphinx `:param:` fields).
- With the default `--allow-init-docstring=False`, keep both sections in the
  class docstring. When the option is `True`, the constructor arguments may
  instead be documented under `__init__()`. The "Attributes" section always
  stays in the class docstring.

## 1. NumPy style

```python
class MyPet:
    """
    A class to hold information of my pet.

    Attributes
    ----------
    name : str
        Name of my pet
    age_in_months : int
        Age of my pet (unit: months)
    weight_in_kg : float
        Weight of my pet (unit: kg)
    is_very_cute_or_not : bool
        Is my pet very cute?  Or just cute?

    Parameters
    ----------
    airtag_id : int
        The ID of the AirTag that I put on my pet
    """
    name: str
    age_in_months: int
    weight_in_kg: float
    is_very_cute_or_not: bool = True

    def __init__(self, airtag_id: int) -> None:
        self.airtag_id = airtag_id
```

The example uses the default `--allow-init-docstring=False`. When the option is
`True`, the constructor arguments may use a separate docstring:

```python
class MyPet:
    """
    A class to hold information of my pet.

    Attributes
    ----------
    name : str
        Name of my pet
    age_in_months : int
        Age of my pet (unit: months)
    weight_in_kg : float
        Weight of my pet (unit: kg)
    is_very_cute_or_not : bool
        Is my pet very cute?  Or just cute?
    """
    name: str
    age_in_months: int
    weight_in_kg: float
    is_very_cute_or_not: bool = True

    def __init__(self, airtag_id: int) -> None:
        """
        Initialize a class object.

        Parameters
        ----------
        airtag_id : int
            The ID of the AirTag that I put on my pet
        """
        self.airtag_id = airtag_id
```

## 2. Google style

```python
class MyPet:
    """
    A class to hold information of my pet.

    Attributes:
        name (str): Name of my pet
        age_in_months (int): Age of my pet (unit: months)
        weight_in_kg (float): Weight of my pet (unit: kg)
        is_very_cute_or_not (bool): Is my pet very cute?  Or just cute?

    Args:
        airtag_id (int): The ID of the AirTag that I put on my pet
    """
    name: str
    age_in_months: int
    weight_in_kg: float
    is_very_cute_or_not: bool = True

    def __init__(self, airtag_id: int) -> None:
        self.airtag_id = airtag_id
```

As in the NumPy example, `--allow-init-docstring=True` permits a separate
`__init__()` docstring.

## 3. Sphinx style

```python
class MyPet:
    """
    A class to hold information of my pet.

    .. attribute :: name
        :type: str

        Name of my pet

    .. attribute :: age_in_months
        :type: int

        Age of my pet (unit: months)

    .. attribute :: weight_in_kg
        :type: float

        Weight of my pet (unit: kg)

    .. attribute :: is_very_cute_or_not
        :type: bool

        Is my pet very cute?  Or just cute?

    :param airtag_id: The ID of the AirTag that I put on my pet
    :type airtag_id: int
    """
    name: str
    age_in_months: int
    weight_in_kg: float
    is_very_cute_or_not: bool = True

    def __init__(self, airtag_id: int) -> None:
        self.airtag_id = airtag_id
```

## 4. Special note: inline docstrings

[PEP 257](https://peps.python.org/pep-0257/) defines a string literal
immediately after an assignment as an attribute docstring. Set
`--require-inline-class-var-docs=True` to require this form (the default is
`False`). When enabled, document every class attribute inline and omit the
"Attributes" section from the class docstring.

An inline docstring may begin with the attribute's type and a colon:

```python
class MyClass:
    """My class that does things."""

    field1 = 5
    """int: My first field"""
```

Inline attribute docstrings work with all three supported styles.

## 5. Private, underscore-only, and special names

The following options control private, underscore-only, and special-dunder
names:

- Class attributes
  - Private (`_value`): `--ignore-private-class-attributes` (default: `True`)
  - Underscore-only (`_`): `--ignore-underscore-only-class-attributes`
    (default: `True`)
  - Special-dunder (`__slots__`): `--ignore-special-dunder-class-attributes`
    (default: `True`)
- Function arguments
  - Private (`_value`): `--ignore-private-args` (default: `False`)
  - Special-dunder (`__value__`): `--ignore-private-args` (default: `False`)
  - Underscore-only (`_`): `--ignore-underscore-only-args` (default: `True`)

"Ignore" means exclude from comparison, not make optional. An ignored name must
not appear in the docstring; documenting it produces an extra-name violation
(`DOC602` and `DOC603` for class attributes).

Special-dunder methods such as `__init__` are always checked, even when
`--skip-checking-private-functions=True`.

To ignore `_: dataclasses.KW_ONLY` while requiring private attributes such as
`_value`, use:

```toml
ignore-private-class-attributes = false
ignore-underscore-only-class-attributes = true
```

See
[name categories](https://jsh9.github.io/pydoclint/config_options.html#name-categories)
for the complete classification rules.
