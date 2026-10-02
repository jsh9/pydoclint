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
    def abstract_generator_with_return_value(
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
    def abstract_generator_documented_as_returned(
        self, var1: str
    ) -> Generator[str, None, None]:
        """Abstract generator whose "Returns" section has the whole annotation.

        No violations in this method: when the generator's return type is
        `None`, the "Returns" section is compared with the whole annotation,
        as it is for a real generator that only yields.

        :param var1: Variable.
        :type var1: str

        :yield: Paths to the files and directories listed.
        :ytype: str

        :return: The generator of paths.
        :rtype: Generator[str, None, None]
        """
