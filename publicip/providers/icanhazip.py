"""icanhazip.com IP provider."""

import httpx

from publicip.providers.base import IPProvider


class ICanHazIpProvider(IPProvider):
    _URL = "https://icanhazip.com"

    @property
    def name(self) -> str:
        return "icanhazip"

    def get_ip(self) -> str:
        response = httpx.get(self._URL, timeout=5)
        response.raise_for_status()
        return response.text.strip()
