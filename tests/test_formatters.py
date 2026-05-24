"""Unit tests for output formatters."""

import json

from publicip.formatters.json_fmt import JsonFormatter
from publicip.formatters.plain import PlainFormatter


class TestPlainFormatter:
    def test_returns_ip_only_when_not_verbose(self) -> None:
        assert PlainFormatter().format("1.2.3.4", "ipify", verbose=False) == "1.2.3.4"

    def test_includes_provider_when_verbose(self) -> None:
        result = PlainFormatter().format("1.2.3.4", "ipify", verbose=True)
        assert "1.2.3.4" in result
        assert "ipify" in result


class TestJsonFormatter:
    def test_returns_ip_field(self) -> None:
        data = json.loads(JsonFormatter().format("1.2.3.4", "ipify", verbose=False))
        assert data["ip"] == "1.2.3.4"
        assert "provider" not in data

    def test_includes_provider_field_when_verbose(self) -> None:
        data = json.loads(JsonFormatter().format("1.2.3.4", "ipify", verbose=True))
        assert data["ip"] == "1.2.3.4"
        assert data["provider"] == "ipify"
