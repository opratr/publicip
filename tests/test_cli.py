"""Unit tests for the CLI entry point."""

import json
import sys

import pytest

from publicip.cli import main


def run(*args: str) -> None:
    sys.argv = ["publicip", *args]
    main()


class TestDefaultBehavior:
    def test_prints_ip(self, httpx_mock, capsys):  # type: ignore[no-untyped-def]
        httpx_mock.add_response(
            url="https://api.ipify.org?format=json", json={"ip": "1.2.3.4"}
        )
        run()
        assert capsys.readouterr().out.strip() == "1.2.3.4"

    def test_verbose_includes_provider(self, httpx_mock, capsys):  # type: ignore[no-untyped-def]
        httpx_mock.add_response(
            url="https://api.ipify.org?format=json", json={"ip": "1.2.3.4"}
        )
        run("--verbose")
        out = capsys.readouterr().out
        assert "1.2.3.4" in out
        assert "ipify" in out

    def test_json_format(self, httpx_mock, capsys):  # type: ignore[no-untyped-def]
        httpx_mock.add_response(
            url="https://api.ipify.org?format=json", json={"ip": "1.2.3.4"}
        )
        run("--format", "json")
        data = json.loads(capsys.readouterr().out)
        assert data["ip"] == "1.2.3.4"
        assert "provider" not in data

    def test_json_format_verbose(self, httpx_mock, capsys):  # type: ignore[no-untyped-def]
        httpx_mock.add_response(
            url="https://api.ipify.org?format=json", json={"ip": "1.2.3.4"}
        )
        run("--format", "json", "--verbose")
        data = json.loads(capsys.readouterr().out)
        assert data["ip"] == "1.2.3.4"
        assert data["provider"] == "ipify"


class TestProviderFlag:
    def test_forces_specific_provider(self, httpx_mock, capsys):  # type: ignore[no-untyped-def]
        httpx_mock.add_response(url="https://icanhazip.com", text="5.6.7.8\n")
        run("--provider", "icanhazip")
        assert capsys.readouterr().out.strip() == "5.6.7.8"

    def test_invalid_provider_exits(self):  # type: ignore[no-untyped-def]
        sys.argv = ["publicip", "--provider", "nonexistent"]
        with pytest.raises(SystemExit):
            main()


class TestAllFlag:
    def test_prints_all_providers(self, httpx_mock, capsys):  # type: ignore[no-untyped-def]
        httpx_mock.add_response(
            url="https://api.ipify.org?format=json", json={"ip": "1.2.3.4"}
        )
        httpx_mock.add_response(url="https://icanhazip.com", text="1.2.3.4\n")
        httpx_mock.add_response(url="https://api.ident.me", text="1.2.3.4\n")
        httpx_mock.add_response(url="https://ip4.seeip.org", text="1.2.3.4\n")
        run("--all")
        out = capsys.readouterr().out
        assert "ipify" in out
        assert "icanhazip" in out
        assert "ident.me" in out
        assert "seeip" in out

    def test_failed_provider_goes_to_stderr(self, httpx_mock, capsys):  # type: ignore[no-untyped-def]
        httpx_mock.add_response(
            url="https://api.ipify.org?format=json", status_code=503
        )
        httpx_mock.add_response(url="https://icanhazip.com", text="1.2.3.4\n")
        httpx_mock.add_response(url="https://api.ident.me", text="1.2.3.4\n")
        httpx_mock.add_response(url="https://ip4.seeip.org", text="1.2.3.4\n")
        run("--all")
        err = capsys.readouterr().err
        assert "ERROR" in err


class TestFallback:
    def test_falls_back_when_primary_fails(self, httpx_mock, capsys):  # type: ignore[no-untyped-def]
        httpx_mock.add_response(
            url="https://api.ipify.org?format=json", status_code=503
        )
        httpx_mock.add_response(url="https://icanhazip.com", text="9.8.7.6\n")
        run()
        assert capsys.readouterr().out.strip() == "9.8.7.6"

    def test_exits_with_code_1_when_all_fail(self, httpx_mock, capsys):  # type: ignore[no-untyped-def]
        httpx_mock.add_response(
            url="https://api.ipify.org?format=json", status_code=503
        )
        httpx_mock.add_response(url="https://icanhazip.com", status_code=503)
        httpx_mock.add_response(url="https://api.ident.me", status_code=503)
        httpx_mock.add_response(url="https://ip4.seeip.org", status_code=503)
        with pytest.raises(SystemExit) as exc_info:
            run()
        assert exc_info.value.code == 1
