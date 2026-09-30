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

        The linter will complain about not having a return section, just like
        it does for abstract methods: without a body to look at, an `Iterator`
        annotation means that the method returns an iterator. (In a .py file,
        this method would also get DOC403.)

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
