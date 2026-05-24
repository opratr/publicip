"""Unit tests for the Resolver."""

import pytest

from publicip.providers.base import IPProvider
from publicip.resolver import Resolver


class SuccessProvider(IPProvider):
    def __init__(self, name: str, ip: str) -> None:
        self._name = name
        self._ip = ip

    @property
    def name(self) -> str:
        return self._name

    def get_ip(self) -> str:
        return self._ip


class FailingProvider(IPProvider):
    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def get_ip(self) -> str:
        raise RuntimeError("network error")


class TestResolver:
    def test_returns_first_provider_result(self) -> None:
        resolver = Resolver(
            [SuccessProvider("a", "1.1.1.1"), SuccessProvider("b", "2.2.2.2")]
        )
        ip, provider = resolver.resolve()
        assert ip == "1.1.1.1"
        assert provider == "a"

    def test_falls_back_to_next_provider_on_failure(self) -> None:
        resolver = Resolver([FailingProvider("a"), SuccessProvider("b", "2.2.2.2")])
        ip, provider = resolver.resolve()
        assert ip == "2.2.2.2"
        assert provider == "b"

    def test_raises_when_all_providers_fail(self) -> None:
        resolver = Resolver([FailingProvider("a"), FailingProvider("b")])
        with pytest.raises(RuntimeError, match="All providers failed"):
            resolver.resolve()

    def test_raises_with_empty_providers(self) -> None:
        with pytest.raises(ValueError):
            Resolver([])

    def test_resolve_all_returns_results_for_every_provider(self) -> None:
        resolver = Resolver([SuccessProvider("a", "1.1.1.1"), FailingProvider("b")])
        results = resolver.resolve_all()
        assert len(results) == 2
        assert results[0] == ("a", "1.1.1.1", None)
        assert results[1][0] == "b"
        assert results[1][2] is not None
