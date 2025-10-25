class CustomError(Exception):
    pass


class B:
    def func1(self, arg1) -> None:
        """
        Do something

        :param arg1: Arg 1
        :return: None
        :rtype: None
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

        :raises: CurtomError: When something goes wrong
        """
        raise CustomError('CustomError')

    def func5(self):
        """
        Do something

        :return: Result
        :rtype: int
        :raises: TypeError: When something goes wrong
        """

        def func5_child1():
            raise ValueError

        return 1

    def func6(self, arg1):
        """
        Do something

        :param arg1: Arg1
        :return: Result
        :rtype: int
        :raises: TypeError: When something goes wrong
        """
        if arg1 is None:
            raise TypeError

        return arg1 + 2

    def func7(self, arg1):
        """
        Do something

        :param arg1: Arg1
        :return: Result
        :rtype: int
        :raises: TypeError: When something goes wrong
        """
        return 2

    def func8(self) -> None:
        """This is a function.

        :raises: FileNotFoundError: If the file does not exist.
        """
        try:
            open('nonexistent')
        except FileNotFoundError:
            raise

    def func9a(self, arg0) -> None:
        """
        There should be DOC502 for this outer method.

        :param arg0: Arg 0
        :raises: FileNotFoundError: If the file does not exist.
        """

        def inner9a(arg1) -> None:
            """
            There should be DOC501 for this inner method

            :param arg1: Arg 1
            """
            try:
                open('nonexistent')
            except FileNotFoundError:
                raise

        print(arg0)

    def func9b(self, arg0) -> None:
        """
        There should not be any violations in this outer method.

        :param arg0: Arg 0
        """

        def inner9a(arg1) -> None:
            """
            There should not be any violations in this inner method.

            :param arg1: Arg1
            :raises: FileNotFoundError: If the file does not exist.
            """
            try:
                open('nonexistent')
            except FileNotFoundError:
                raise

        print(arg0)

    def func11(self, arg0) -> None:
        """
        This docstring doesn't specify all the raised exceptions.

        :param arg0: Arg 0
        :raises TypeError: if arg0 is zero.
        """
        if arg0 == 0:
            raise TypeError
        raise ValueError

    def func12(self, arg0) -> None:
        """
        There should not be any violations in this method.

        :param arg0: Arg 0
        :raises TypeError: if arg0 is zero.
        :raises ValueError: otherwise.
        """
        if arg0 == 0:
            raise TypeError
        raise ValueError

    def func13(self) -> None:
        """
        Should raise an error due to duplicated raises.

        :raises ValueError: all the time.
        :raises ValueError: typo!
        """
        raise ValueError

    def func14(self) -> None:
        """
        Should fail, expects `exceptions.CustomError`.

        :raises CustomError: every time.
        """
        exceptions = object()
        exceptions.CustomError = CustomError
        raise exceptions.CustomError()

    def func15(self) -> None:
        """
        Should fail, expects `exceptions.m.CustomError`.

        :raises CustomError: every time.
        """
        exceptions = object()
        exceptions.m = object()
        exceptions.m.CustomError = CustomError
        raise exceptions.m.CustomError

    def func16(self) -> None:
        """
        It should pass.

        :raises MyException: if a < 1
        :raises YourException: if a < 2
        :raises a.b.c.TheirException: if a < 3
        :raises a.b.c.d.e.f.g.WhoseException: if a < 4
        """
        if a < 1:
            raise MyException.a.b.c(('a', 'b'))
        elif a < 2:
            raise YourException.a.b.c(1)
        elif a < 3:
            raise a.b.c.TheirException.from_str.d.e('my_str')
        elif a < 4:
            raise a.b.c.d.e.f.g.WhoseException.h.i.j.k
        else:
            pass

    def func17(self) -> None:
        """
        When --should-declare-assert-error-if-assert-statement-exists is True:

        It should pass.

        :raises AssertionError: every time, without a message.
        """
        assert False

    def func18(self) -> None:
        """
        When --should-declare-assert-error-if-assert-statement-exists is True:

        It should pass.

        :raises AssertionError: every time, with a message.
        """
        assert False, 'False'

    def func19(self) -> None:
        """
        When --should-declare-assert-error-if-assert-statement-exists is True:

        Should fail, expects `AssertionError`.

        :return: None
        :rtype: None
        """
        assert False

    def func20(self) -> None:
        """
        When --should-declare-assert-error-if-assert-statement-exists is True:

        It should pass.

        :raises AssertionError123: every time, with a message.
        """
        assert False, 'False'
