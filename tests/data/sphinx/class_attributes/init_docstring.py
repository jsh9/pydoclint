class MyClass1:
    """
    A class that holds some things.


    :attr name: The name
    :type name: str
    :attr indices: The indices
    :type indices: int
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
