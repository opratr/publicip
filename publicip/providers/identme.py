"""ident.me IP provider."""

import httpx

from publicip.providers.base import IPProvider


class IdentMeProvider(IPProvider):
    _URL = "https://4.ident.me"

    @property
    def name(self) -> str:
        return "ident.me"

    def get_ip(self) -> str:
        response = httpx.get(self._URL, timeout=5)
        response.raise_for_status()
        return response.text.strip()
