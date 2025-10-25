class A:
    def __init__(self):
        pass

    @property
    def attr1(self):
        """Return the 1st attribute"""
        return 1


class B:
    def __init__(self):
        pass

    @property
    def attr1(self) -> int:
        """
        Return the 1st attribute

        Returns
        -------
        int
            the 1st attribute
        """
        return 1
