"""Unit tests for individual IP providers."""

import httpx
import pytest
from pytest_httpx import HTTPXMock

from publicip.providers.icanhazip import ICanHazIpProvider
from publicip.providers.identme import IdentMeProvider
from publicip.providers.ipify import IpifyProvider
from publicip.providers.seeip import SeeIpProvider


class TestIpifyProvider:
    def test_returns_ip_from_json(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url="https://api.ipify.org?format=json", json={"ip": "1.2.3.4"}
        )
        assert IpifyProvider().get_ip() == "1.2.3.4"

    def test_raises_on_http_error(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url="https://api.ipify.org?format=json", status_code=503
        )
        with pytest.raises(httpx.HTTPStatusError):
            IpifyProvider().get_ip()

    def test_name(self) -> None:
        assert IpifyProvider().name == "ipify"


class TestICanHazIpProvider:
    def test_returns_stripped_ip(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(url="https://icanhazip.com", text="5.6.7.8\n")
        assert ICanHazIpProvider().get_ip() == "5.6.7.8"

    def test_name(self) -> None:
        assert ICanHazIpProvider().name == "icanhazip"


class TestIdentMeProvider:
    def test_returns_stripped_ip(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(url="https://api.ident.me", text="9.10.11.12\n")
        assert IdentMeProvider().get_ip() == "9.10.11.12"

    def test_name(self) -> None:
        assert IdentMeProvider().name == "ident.me"


class TestSeeIpProvider:
    def test_returns_stripped_ip(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(url="https://ip4.seeip.org", text="13.14.15.16\n")
        assert SeeIpProvider().get_ip() == "13.14.15.16"

    def test_name(self) -> None:
        assert SeeIpProvider().name == "seeip"
