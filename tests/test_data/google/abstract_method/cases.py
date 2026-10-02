from abc import ABC, abstractmethod
from collections.abc import Generator, Iterator


class AbstractClass(ABC):
    """Example abstract class."""

    @abstractmethod
    @something
    @something_else
    def abstract_method(self, var1: str) -> Generator[str, None, None]:
        """Abstract method.

        No violations in this method.

        Args:
            var1 (str): Variable.

        Raises:
            ValueError: Example exception

        Yields:
            str: Paths to the files and directories listed.
        """

    @abstractmethod
    @hello
    @world
    def another_abstract_method(self, var1: str) -> Iterator[str]:
        """Another abstract method.

        No violations in this method. Without a body to look at, the "Yields"
        section shows that the method yields (rather than returning an
        iterator), so it doesn't need a "Returns" section.

        Args:
            var1 (str): Variable.

        Raises:
            ValueError: Example exception

        Yields:
            str: Paths to the files and directories listed.
        """

    @abstractmethod
    @good
    @morning
    def third_abstract_method(self, var1: str) -> str:
        """The 3rd abstract method.

        The linter will complain about not having a return section.

        Args:
            var1 (str): Variable.

        Raises:
            ValueError: Example exception
        """

    @abstractmethod
    def abstractGeneratorWithReturnValue(
        self, var1: str
    ) -> Generator[str, None, int]:
        """Abstract generator that returns a value at the end.

        No violations in this method: the "Returns" section documents the
        generator's return type (`int` in `Generator[str, None, int]`), as it
        would for the real generator.

        Args:
            var1 (str): Variable.

        Yields:
            str: Paths to the files and directories listed.

        Returns:
            int: How many paths were listed.
        """

    @abstractmethod
    def abstractGeneratorDocumentedAsReturned(
        self, var1: str
    ) -> Generator[str, None, None]:
        """Abstract generator whose "Returns" section has the whole annotation.

        No violations in this method: the "Returns" section can have the whole
        annotation, as for a real generator that only yields.

        Args:
            var1 (str): Variable.

        Yields:
            str: Paths to the files and directories listed.

        Returns:
            Generator[str, None, None]: The generator of paths.
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

        Args:
            var1 (str): Variable.

        Yields:
            str: Paths to the files and directories listed.

        Returns:
            Generator[str, None, int]: The generator of paths.
        """

    @abstractmethod
    def abstractIteratorThatReturns(self, var1: str) -> Iterator[str]:
        """Abstract method whose body returns an iterator.

        The linter will complain about not having a return section: the body
        has a "return" statement, so it returns an iterator, and the "Yields"
        section doesn't change that.

        Args:
            var1 (str): Variable.

        Yields:
            str: Paths to the files and directories listed.
        """
        return iter([var1])

    @abstractmethod
    def abstractMethodWithoutReturnAnnotation(self, var1: str):
        """Abstract method that documents what it returns, without annotation.

        The linter will complain that the "Returns" section doesn't match the
        missing return annotation (DOC203) when return types are checked, but
        not that there are no "return" statements (DOC202): the body is a
        placeholder.

        Args:
            var1 (str): Variable.

        Returns:
            int: The result.
        """
