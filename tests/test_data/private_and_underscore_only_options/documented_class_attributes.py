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
    __tablename__
        A special dunder attribute.
    """

    public: int
    _private: str
    _: bool
    __: float
    __tablename__: str
