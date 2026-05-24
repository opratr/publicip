"""Abstract base for IP providers."""

from abc import ABC, abstractmethod


class IPProvider(ABC):
    """Contract every IP provider must satisfy."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable provider name."""

    @abstractmethod
    def get_ip(self) -> str:
        """Return the public IP address string, or raise on failure."""
