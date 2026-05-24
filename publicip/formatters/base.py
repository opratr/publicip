"""Abstract base for output formatters."""

from abc import ABC, abstractmethod


class OutputFormatter(ABC):
    @abstractmethod
    def format(self, ip: str, provider: str, verbose: bool) -> str:
        """Return a formatted string representation of the result."""
