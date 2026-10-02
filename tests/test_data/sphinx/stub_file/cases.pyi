# Default-value fixtures use checkArgDefaults=True, which Visitor.__init__
# rejects for Sphinx style. There is therefore no Sphinx defaults.pyi fixture.
# This file covers stub-body behavior and argument types with that check off.

from collections.abc import Generator, Iterator

class StubClass:
    """Example class in a stub file."""

    def documentsRaises(self, var1: str) -> str:
        """Method that documents an exception.

        No violations in this method. (In a .py file, this method would get
        DOC502, because its body has no "raise" statements.)

        :param var1: Variable.
        :type var1: str

        :return: The result.
        :rtype: str

        :raises: ValueError: Example exception
        """
        ...

    def documentsYields(self, var1: str) -> Generator[str, None, None]:
        """Method that documents what it yields.

        No violations in this method. (In a .py file, this method would get
        DOC403, because its body has no "yield" statements.)

        :param var1: Variable.
        :type var1: str

        :yield: Paths to the files and directories listed.
        :ytype: str
        """
        ...

    def documentsYieldsWithIterator(self, var1: str) -> Iterator[str]:
        """Method annotated with `Iterator` that documents what it yields.

        No violations in this method. Without a body to look at, the "Yields"
        section shows that the method yields (rather than returning an
        iterator), so it doesn't need a "Returns" section. (In a .py file, this
        method would get DOC201 and DOC403.)

        :param var1: Variable.
        :type var1: str

        :yield: Paths to the files and directories listed.
        :ytype: str
        """
        ...

    def documentsNothingWithIterator(self, var1: str) -> Iterator[str]:
        """Method annotated with `Iterator` that documents neither section.

        The linter will complain about not having a return section: without a
        "Yields" section, nothing shows that the method yields.

        :param var1: Variable.
        :type var1: str
        """
        ...

    def documentsYieldsWithNonGeneratorAnnotation(self, var1: str) -> None:
        """Method that documents what it yields, but can't yield anything.

        The linter will complain about the "Yields" section. Without a body to
        look at, the return annotation is the only evidence of what the method
        does, and `None` isn't a Generator, Iterator, or Iterable.

        :param var1: Variable.
        :type var1: str

        :yield: Paths to the files and directories listed.
        :ytype: str
        """
        ...

    def hasWrongArgType(self, var1: str) -> None:
        """Method whose docstring has the wrong argument type.

        The linter will complain about the type mismatch, because checks that
        don't depend on the function body still run in stub files.

        :param var1: Variable.
        :type var1: int
        """
        ...
