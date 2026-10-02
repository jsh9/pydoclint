from abc import ABC, abstractmethod
from collections.abc import Generator, Iterator


class AbstractClass(ABC):
    """Example abstract class."""

    @abstractmethod
    def abstract_method(self, var1: str) -> Generator[str, None, None]:
        """Abstract method.

        No violations in this method.

        :param var1: Variable.
        :type var1: str

        :raises: ValueError: Example exception

        :yield: Paths to the files and directories listed.
        :ytype: str
        """

    @abstractmethod
    def another_abstract_method(self, var1: str) -> Iterator[str]:
        """Another abstract method.

        No violations in this method. Without a body to look at, the "Yields"
        section shows that the method yields (rather than returning an
        iterator), so it doesn't need a "Returns" section.

        :param var1: Variable.
        :type var1: str

        :raises: ValueError: Example exception

        :yield: Paths to the files and directories listed.
        :ytype: str
        """

    @abstractmethod
    def third_abstract_method(self, var1: str) -> str:
        """The 3rd abstract method.

        The linter will complain about not having a return section.

        :param var1: Variable.
        :type var1: str

        :raises: ValueError: Example exception
        """

    @abstractmethod
    def abstractGeneratorWithReturnValue(
        self, var1: str
    ) -> Generator[str, None, int]:
        """Abstract generator that returns a value at the end.

        No violations in this method: the "Returns" section documents the
        generator's return type (`int` in `Generator[str, None, int]`), as it
        would for the real generator.

        :param var1: Variable.
        :type var1: str

        :yield: Paths to the files and directories listed.
        :ytype: str

        :return: How many paths were listed.
        :rtype: int
        """

    @abstractmethod
    def abstractGeneratorDocumentedAsReturned(
        self, var1: str
    ) -> Generator[str, None, None]:
        """Abstract generator whose "Returns" section has the whole annotation.

        No violations in this method: the "Returns" section can have the whole
        annotation, as for a real generator that only yields.

        :param var1: Variable.
        :type var1: str

        :yield: Paths to the files and directories listed.
        :ytype: str

        :return: The generator of paths.
        :rtype: Generator[str, None, None]
        """

    @abstractmethod
    def abstractGeneratorWithReturnValueDocumentedAsReturned(
        self, var1: str
    ) -> Generator[str, None, int]:
        """Abstract generator returning a value, documented as a whole.

        No violations in this method: the "Returns" section has the whole
        annotation instead of the generator's return type (`int`). Without a
        body, nothing shows whether the generator returns a value, so both are
        accepted.

        :param var1: Variable.
        :type var1: str

        :yield: Paths to the files and directories listed.
        :ytype: str

        :return: The generator of paths.
        :rtype: Generator[str, None, int]
        """

    @abstractmethod
    def abstractIteratorThatReturns(self, var1: str) -> Iterator[str]:
        """Abstract method whose body returns an iterator.

        The linter will complain about not having a return section: the body
        has a "return" statement, so it returns an iterator, and the "Yields"
        section doesn't change that.

        :param var1: Variable.
        :type var1: str

        :yield: Paths to the files and directories listed.
        :ytype: str
        """
        return iter([var1])

    @abstractmethod
    def abstractMethodWithoutReturnAnnotation(self, var1: str):
        """Abstract method that documents what it returns, without annotation.

        The linter will complain that the "Returns" section doesn't match the
        missing return annotation (DOC203) when return types are checked, but
        not that there are no "return" statements (DOC202): the body is a
        placeholder.

        :param var1: Variable.
        :type var1: str

        :return: The result.
        :rtype: int
        """
