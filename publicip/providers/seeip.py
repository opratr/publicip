"""seeip.org IP provider."""

import httpx

from publicip.providers.base import IPProvider


class SeeIpProvider(IPProvider):
    _URL = "https://ipv4.seeip.org"

    @property
    def name(self) -> str:
        return "seeip"

    def get_ip(self) -> str:
        response = httpx.get(self._URL, timeout=5)
        response.raise_for_status()
        return response.text.strip()
