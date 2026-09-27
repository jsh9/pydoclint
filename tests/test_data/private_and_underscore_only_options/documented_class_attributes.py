class Example:
    """
    Class with attributes from every name category.

    Attributes
    ----------
    public
        A public attribute.
    _private
        A private attribute.
    _
        An underscore-only attribute.
    __
        Another underscore-only attribute.
    __slots__
        Special protocol metadata.
    __hash__
        Special protocol metadata.
    __match_args__
        Special protocol metadata.
    """

    public: int
    _private: str
    _: bool
    __: float
    __slots__: tuple[str, ...]
    __hash__ = None
    __match_args__: tuple[str, ...]
