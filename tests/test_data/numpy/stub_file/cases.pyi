from collections.abc import Generator, Iterator

class StubClass:
    """Example class in a stub file."""

    def documentsRaises(self, var1: str) -> str:
        """Method that documents an exception.

        No violations in this method. (In a .py file, this method would get
        DOC502, because its body has no "raise" statements.)

        Parameters
        ----------
        var1 : str
            Variable.

        Returns
        -------
        str
            The result.

        Raises
        ------
        ValueError
            Example exception
        """
        ...

    def documentsYields(self, var1: str) -> Generator[str, None, None]:
        """Method that documents what it yields.

        No violations in this method. (In a .py file, this method would get
        DOC403, because its body has no "yield" statements.)

        Parameters
        ----------
        var1 : str
            Variable.

        Yields
        ------
        str
            Paths to the files and directories listed.
        """
        ...

    def documentsYieldsWithIterator(self, var1: str) -> Iterator[str]:
        """Method annotated with `Iterator` that documents what it yields.

        The linter will complain about not having a return section, just like
        it does for abstract methods: without a body to look at, an `Iterator`
        annotation means that the method returns an iterator. (In a .py file,
        this method would also get DOC403.)

        Parameters
        ----------
        var1 : str
            Variable.

        Yields
        ------
        str
            Paths to the files and directories listed.
        """
        ...

    def hasWrongArgType(self, var1: str) -> None:
        """Method whose docstring has the wrong argument type.

        The linter will complain about the type mismatch, because checks that
        don't depend on the function body still run in stub files.

        Parameters
        ----------
        var1 : int
            Variable.
        """
        ...
