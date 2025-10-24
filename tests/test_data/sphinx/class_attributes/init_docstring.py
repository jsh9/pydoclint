class MyClass1:
    """
    A class that holds some things.

    .. attribute :: name
        :type: str

        The name

    .. attribute :: indices
        :type: int

        The indices
    """

    name: str
    index: int

    hello: int = 1
    world: dict

    def __init__(self, arg1: int) -> None:
        """
        Initialize the class object

        :param arg1: The information
        :type arg1: float
        """
        self.arg1 = arg1
