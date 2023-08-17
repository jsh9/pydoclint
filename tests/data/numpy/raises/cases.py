class CustomError(Exception):
    pass


class B:
    def func1(self, arg1) -> None:
        """
        Do something

        Parameters
        ----------
        arg1
            Arg 1

        Returns
        -------
        None
        """
        a = 1
        b = 2
        raise ValueError('Hello world')

    def func2(self):
        raise Exception

    def func3(self, arg1):
        """Do something"""
        if arg1 > 2:
            raise TypeError

    def func4(self):
        """
        Do something.

        Raises
        ------
        CurtomError
            When something goes wrong
        """
        raise CustomError('CustomError')

    def func5(self):
        """
        Do something

        Returns
        -------
        int
            Result

        Raises
        ------
        TypeError
            When something goes wrong
        """

        def func5_child1():
            raise ValueError

        return 1

    def func6(self, arg1):
        """
        Do something

        Parameters
        ----------
        arg1
            Arg 1

        Returns
        -------
        int
            Result

        Raises
        ------
        TypeError
            When something goes wrong
        """
        if arg1 is None:
            raise TypeError

        return arg1 + 2

    def func7(self, arg1):
        """
        Do something

        Parameters
        ----------
        arg1
            Arg 1

        Returns
        -------
        int
            Result

        Raises
        ------
        Exception
            When something goes wrong
        """
        return 2

    def func8(self) -> None:
        """This is a function.

        Raises
        ------
        FileNotFoundError
            If the file does not exist.
        """
        try:
            open('nonexistent')
        except FileNotFoundError:
            raise

    def func9a(self, arg0) -> None:
        """
        There should be DOC502 for this outer method.

        Parameters
        ----------
        arg0 :
            Arg 0

        Raises
        ------
        FileNotFoundError
            If the file does not exist.
        """

        def inner9a(arg1) -> None:
            """
            There should be DOC501 for this inner method

            Parameters
            ----------
            arg1
                Arg 1
            """
            try:
                open('nonexistent')
            except FileNotFoundError:
                raise

        print(arg0)

    def func9b(self, arg0) -> None:
        """
        There should not be any violations in this outer method.

        Parameters
        ----------
        arg0
            Arg 0
        """

        def inner9a(arg1) -> None:
            """
            There should not be any violations in this inner method.

            Parameters
            ----------
            arg1
                Arg1

            Raises
            ------
            FileNotFoundError
                If the file does not exist.
            """
            try:
                open('nonexistent')
            except FileNotFoundError:
                raise

        print(arg0)

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
