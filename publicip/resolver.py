"""Queries providers in priority order with automatic fallback."""

from publicip.providers.base import IPProvider


class Resolver:
    def __init__(self, providers: list[IPProvider]) -> None:
        if not providers:
            raise ValueError("At least one provider is required")
        self._providers = providers

    def resolve(self) -> tuple[str, str]:
        """Return (ip, provider_name) from the first provider that succeeds."""
        errors: list[str] = []
        for provider in self._providers:
            try:
                ip = provider.get_ip()
                return ip, provider.name
            except Exception as exc:
                errors.append(f"{provider.name}: {exc}")
        raise RuntimeError("All providers failed:\n" + "\n".join(errors))

    def resolve_all(self) -> list[tuple[str, str, str | None]]:
        """Return (provider_name, ip_or_none, error_or_none) for every provider."""
        results: list[tuple[str, str, str | None]] = []
        for provider in self._providers:
            try:
                ip = provider.get_ip()
                results.append((provider.name, ip, None))
            except Exception as exc:
                results.append((provider.name, "", str(exc)))
        return results
