from typing import Annotated, Literal


class Config:
    """
    Class whose attributes have placeholder defaults.

    Attributes:
        retries (int, default=3): How many times to retry. (Any documented
            default is fine.)
        timeout (float): How long to wait, in seconds. (No documented default
            is also fine.)
        name (int, default='main'): Wrong type: the class attribute is a
            ``str``, so the linter will complain about the type mismatch.
    """

    retries: int = ...
    timeout: float = ...
    name: str = ...

def connect(
    host: str,
    port: int = ...,
    verbose: bool = ...,
    label: str = ...,
) -> None:
    """
    Function whose arguments have placeholder defaults.

    Args:
        host (str): Host name.
        port (int, default=8080): Port number. (Any documented default is
            fine.)
        verbose (bool): Whether to log. (No documented default is also fine.)
        label (int): Wrong type: the argument is a ``str``, so the linter will
            complain about the type mismatch.
    """
    ...

class AnnotationDefaults:
    """
    Attributes whose type annotations contain default text.

    Attributes:
        annotated (Annotated[int, 'units, default=3'], default=...): The
            metadata must remain part of the type.
        literal (Literal['text, default=3']): The literal must remain intact
            even without a documented default.
        wrongAnnotated (Annotated[str, 'units, default=3'], default=...):
            Wrong type: the actual annotation uses int.
        wrongLiteral (Literal['other, default=3'], default=...): Wrong type:
            the actual literal starts with text.
        customDefault (Annotated[int, 'units, default=3'], default=5): Any
            documented default is allowed only in a stub file.
    """

    annotated: Annotated[int, 'units, default=3'] = ...
    literal: Literal['text, default=3'] = ...
    wrongAnnotated: Annotated[int, 'units, default=3'] = ...
    wrongLiteral: Literal['text, default=3'] = ...
    customDefault: Annotated[int, 'units, default=3'] = ...

def preserveAnnotationDefaults(
    annotated: Annotated[int, 'units, default=3'] = ...,
    literal: Literal['text, default=3'] = ...,
    wrongAnnotated: Annotated[int, 'units, default=3'] = ...,
    wrongLiteral: Literal['text, default=3'] = ...,
    customDefault: Annotated[int, 'units, default=3'] = ...,
) -> None:
    """
    Arguments whose type annotations contain default text.

    Args:
        annotated (Annotated[int, 'units, default=3'], default=...): The
            metadata must remain part of the type.
        literal (Literal['text, default=3']): The literal must remain intact
            even without a documented default.
        wrongAnnotated (Annotated[str, 'units, default=3'], default=...):
            Wrong type: the actual annotation uses int.
        wrongLiteral (Literal['other, default=3'], default=...): Wrong type:
            the actual literal starts with text.
        customDefault (Annotated[int, 'units, default=3'], default=5): Any
            documented default is allowed only in a stub file.
    """
    ...

class BacktickDefaults:
    """
    Attributes whose documented types are wrapped in backticks.

    Attributes:
        placeholder (``int, default=...``): Matches the class attribute
            exactly.
        customDefault (``int, default=3``): Any documented default is allowed
            only in a stub file.
        wrongType (`str, default=3`): Wrong type: the class attribute is an
            ``int``.
    """

    placeholder: int = ...
    customDefault: int = ...
    wrongType: int = ...

def backtickDefaults(
    placeholder: int = ...,
    customDefault: int = ...,
    wrongType: int = ...,
) -> None:
    """
    Arguments whose documented types are wrapped in backticks.

    Args:
        placeholder (``int, default=...``): Matches the argument exactly.
        customDefault (``int, default=3``): Any documented default is allowed
            only in a stub file.
        wrongType (`str, default=3`): Wrong type: the argument is an ``int``.
    """
    ...

def positionalOnlyDefaults(key: str, default: int = ..., /) -> int:
    """
    Function whose positional-only argument has a placeholder default.

    Args:
        key (str): The key.
        default (int, default=0): What to return when the key is missing.
            (Any documented default is fine for positional-only arguments
            too.)

    Returns:
        int: The value.
    """
    ...
