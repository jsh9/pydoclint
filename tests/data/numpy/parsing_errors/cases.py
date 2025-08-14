class A:
    """
    Some class. Even though this is not exactly the
    correct numpy style, it will be considered numpy
    style because it "looks like" numpy style the most.

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
            Something to yield. This is not the correct numpy docstring
            format (because the yielded type is needed), but it won't
            produce DOC001, because this docstring still "looks like"
            numpy style the most.
        """
        pass


def funcWithGoogleStyle(arg1: str, arg2: int) -> str:
    """
    This function uses Google style but will be parsed as numpy.

    Args:
        arg1 (str): First argument description
        arg2 (int): Second argument description

    Returns:
        str: Return value description
    """
    return arg1
