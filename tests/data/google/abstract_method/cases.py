from abc import ABC, abstractmethod
from collections.abc import Generator


class AbstractClass(ABC):
    """Example abstract class."""

    @abstractmethod
    def abstract_method(self, var1: str) -> Generator[str, None, None]:
        """Abstract method.

        Args:
            var1 (str): Variable.

        Raises:
            ValueError: Example exception

        Yields:
            str: Paths to the files and directories listed.
        """
