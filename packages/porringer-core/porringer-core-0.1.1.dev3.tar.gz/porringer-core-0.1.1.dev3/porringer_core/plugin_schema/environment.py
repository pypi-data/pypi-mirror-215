"""Plugin utilities for package environments"""

from abc import abstractmethod
from typing import Protocol

from porringer_core.schema import Package


class EnvironmentPlugin(Protocol):
    """Plugin definition for package environments"""

    @abstractmethod
    def packages(self) -> list[Package]:
        """Gathers packages in the given environment

        Returns:
            A list of packages
        """
        raise NotImplementedError

    @abstractmethod
    def search(self) -> Package | None:
        """Searches the environment's sources for a package

        Returns:
            The package, or None if it doesn't exist
        """
        raise NotImplementedError
