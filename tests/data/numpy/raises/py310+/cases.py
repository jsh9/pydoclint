# This can be merged into the parent folder after Py39 support is dropped.
# Because Python 3.9 does not support match-case syntax.


class B:
    def func10(self, arg0) -> int:
        """
        There should be a DOC501 violation for this function

        Parameters
        ----------
        arg0 :
            Arg 0

        Returns
        -------
        int
            The return value
        """
        match arg0:
            case 1:
                return 1
            case 2:
                return 2
            case _:
                raise ValueError('Hello world')
