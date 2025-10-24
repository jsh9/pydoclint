# This edge case comes from:
#    https://github.com/jsh9/pydoclint/issues/140#issuecomment-2426031940

from dataclasses import dataclass
from typing import ClassVar

from attrs import define, field
from pydantic import BaseModel, Field


@define
class AttrsClass:
    """
    My class.

    Attributes:
        a (bool): my class attribute
        c (float): This is y
    """

    a: ClassVar[bool] = True  # class attribute
    b: int  # instance attribute
    c: float = 1.0  # instance attribute
    d: str = field(default='abc')  # instance attribute


@dataclass
class DataClass:
    """
    My class.

    Attributes:
        e (ClassVar[bool]): my class attribute
    """

    e: ClassVar[bool] = True  # class attribute
    f: int  # instance attribute
    g: float = 1.0  # instance attribute
    h: str = field(default='abc')  # instance attribute


class PydanticClass(BaseModel):
    """
    My class.

    Attributes:
        i (bool): my class attribute
    """

    i: ClassVar[bool] = True  # class attribute
    j: int  # instance attribute
    k: float = 1.0  # instance attribute
    l: str = Field(default='abc')  # instance attribute
