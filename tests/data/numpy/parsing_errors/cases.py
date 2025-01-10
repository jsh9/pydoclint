class A:
    """
    Some class

    Parameters
    ----------
        arg1
        arg2

    Parameters
    ----------
        arg3
        arg4
    """

    def __init__(self):
        pass

    def method1(self, arg3):
        """
        Parameters
        ----------
        arg3 :
            arg 3
        """
        pass

    def method2(self, arg4):
        """
        Yields
        ------
            Something to yield. This is not the correct docstring
            format and will lead to DOC001, because the yielded
            type is needed.
        """
        pass
