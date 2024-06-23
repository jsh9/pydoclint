# Checking class attributes

Class attributes are similar to function arguments. They look like this:

```python
class MyPet:
    name: str
    age_in_months: int
    weight_in_kg: float
    is_very_cute_or_not: bool = True
```

And we'd like to also document them in docstrings. However, none of the
mainstream docstring styles (Google, numpy, or Sphinx) offers explicit
guidelines on documenting class attributes. Therefore, in _pydoclint_, we
designed a new (but not totally surprising) docstring section: "attributes"
under which we can document the class attributes.

Here is an example that demonstrates the expected style:

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

From this example, we can see a few things:

1. The class attributes should be put in a different docstring section than the
   argument passed into the class constructor (`__init__()`)
2. Both the class attributes and the input arguments to `__init__()` are in the
   same docstring. (This is assuming the _pydoclint_ option
   `--allow-init-docstring` is `False`)

If `--allow-init-docstring` is set to `True`, we can write two separate
docstrings like this:

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

#### Special note for Sphinx style docstrings

If you use the Sphinx style, you can annotate class attributes like this:

```python
:attr my_attr: My attribute
:type my_attr: float
```

However, there is no guarantee that this `:attr` tag is recognized by current
doc rendering programs.
