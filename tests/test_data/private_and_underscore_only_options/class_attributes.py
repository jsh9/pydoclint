class Example:
    """
    Class with attributes from every name category.

    Attributes
    ----------
    public
        A public attribute.
    """

    public: int
    _private: str
    _: bool
    __: float
    __slots__: tuple[str, ...]
    __hash__ = None
    __match_args__: tuple[str, ...]
