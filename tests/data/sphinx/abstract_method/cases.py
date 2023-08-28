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

        The linter will complain about not having a return section, because
        if the return type annotation is `Iterator`, it is supposed to be
        returning something, rather than yielding something.  (To yield
        something, use `Generator` as the return type annotation.)

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
