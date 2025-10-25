class MyClass:
    """
    My Class.

    This edge case comes from: https://github.com/jsh9/pydoclint/issues/148

    Attributes:
        attr_1 (str): The first attribute
        attr_2: The 2nd attribute
        attr_3 (float): The 3rd attribute
    """

    attr_1: str = 'hello'
    attr_2 = 4
    attr_3: float
    _hidden_attr: bool
