# This can be merged into the parent folder after Py39 support is dropped.
# Because Python 3.9 does not support match-case syntax.


class B:
    def func10(self, arg0) -> int:
        """
        There should be a DOC501 violation for this function

        :param arg0: Arg 0
        :return: The return value
        """
        match arg0:
            case 1:
                return 1
            case 2:
                return 2
            case _:
                raise ValueError('Hello world')
