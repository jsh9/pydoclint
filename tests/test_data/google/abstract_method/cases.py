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
