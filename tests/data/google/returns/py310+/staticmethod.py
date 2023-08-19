# This can be merged into the parent folder after Py39 support is dropped.
# Because Python 3.9 does not suport match-case syntax.


class MyClass:
    def __init__(self):
        pass

    @staticmethod
    def func11(arg0: str) -> int:
        """
        There should be DOC201 and DOC203 violations for this function

        Args:
            arg0 (str): Arg 0

        Raises:
            ValueError: When there is a value error
        """
        match arg0:
            case 'a':
                return 1
            case 'b':
                return 2
            case _:
                raise ValueError('Hello world')
