class Config:
    """
    Class whose attributes have placeholder defaults.

    Attributes
    ----------
    retries : int, default=3
        How many times to retry. (Any documented default is fine.)
    timeout : float
        How long to wait, in seconds. (No documented default is also fine.)
    name : int, default='main'
        Wrong type: the class attribute is a ``str``, so the linter will
        complain about the type mismatch.
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

    Parameters
    ----------
    host : str
        Host name.
    port : int, default=8080
        Port number. (Any documented default is fine.)
    verbose : bool
        Whether to log. (No documented default is also fine.)
    label : int
        Wrong type: the argument is a ``str``, so the linter will complain
        about the type mismatch.
    """
    ...
