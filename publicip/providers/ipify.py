"""ipify.org IP provider."""

import httpx

from publicip.providers.base import IPProvider


class IpifyProvider(IPProvider):
    _URL = "https://api.ipify.org?format=json"

    @property
    def name(self) -> str:
        return "ipify"

    def get_ip(self) -> str:
        response = httpx.get(self._URL, timeout=5)
        response.raise_for_status()
        return str(response.json()["ip"])
