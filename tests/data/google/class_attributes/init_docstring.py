class MyClass1:
    """
    A class that holds some things.

    Attributes:
        name (str): The name
        indices (int): The indices
    """

    name: str
    index: int

    hello: int = 1
    world: dict

    def __init__(self, arg1: int) -> None:
        """
        Initialize the class object

        Args:
            arg1 (float): The information
        """
        self.arg1 = arg1
