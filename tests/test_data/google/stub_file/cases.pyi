from collections.abc import Generator, Iterator

class StubClass:
    """Example class in a stub file."""

    def documentsRaises(self, var1: str) -> str:
        """Method that documents an exception.

        No violations in this method. (In a .py file, this method would get
        DOC502, because its body has no "raise" statements.)

        Args:
            var1 (str): Variable.

        Returns:
            str: The result.

        Raises:
            ValueError: Example exception
        """
        ...

    def documentsYields(self, var1: str) -> Generator[str, None, None]:
        """Method that documents what it yields.

        No violations in this method. (In a .py file, this method would get
        DOC403, because its body has no "yield" statements.)

        Args:
            var1 (str): Variable.

        Yields:
            str: Paths to the files and directories listed.
        """
        ...

    def documentsYieldsWithIterator(self, var1: str) -> Iterator[str]:
        """Method annotated with `Iterator` that documents what it yields.

        No violations in this method. Without a body to look at, the "Yields"
        section shows that the method yields (rather than returning an
        iterator), so it doesn't need a "Returns" section. (In a .py file, this
        method would get DOC201 and DOC403.)

        Args:
            var1 (str): Variable.

        Yields:
            str: Paths to the files and directories listed.
        """
        ...

    def documentsNothingWithIterator(self, var1: str) -> Iterator[str]:
        """Method annotated with `Iterator` that documents neither section.

        The linter will complain about not having a return section: without a
        "Yields" section, nothing shows that the method yields.

        Args:
            var1 (str): Variable.
        """
        ...

    def documentsYieldsWithNonGeneratorAnnotation(self, var1: str) -> None:
        """Method that documents what it yields, but can't yield anything.

        The linter will complain about the "Yields" section. Without a body to
        look at, the return annotation is the only evidence of what the method
        does, and `None` isn't a Generator, Iterator, or Iterable.

        Args:
            var1 (str): Variable.

        Yields:
            str: Paths to the files and directories listed.
        """
        ...

    def hasWrongArgType(self, var1: str) -> None:
        """Method whose docstring has the wrong argument type.

        The linter will complain about the type mismatch, because checks that
        don't depend on the function body still run in stub files.

        Args:
            var1 (int): Variable.
        """
        ...
