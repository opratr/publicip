"""Command-line entry point."""

import argparse
import sys
from collections.abc import Callable

from publicip.formatters.json_fmt import JsonFormatter
from publicip.formatters.plain import PlainFormatter
from publicip.providers import (
    ICanHazIpProvider,
    IdentMeProvider,
    IpifyProvider,
    IPProvider,
    SeeIpProvider,
)
from publicip.resolver import Resolver

_PROVIDERS: dict[str, Callable[[], IPProvider]] = {
    "ipify": IpifyProvider,
    "icanhazip": ICanHazIpProvider,
    "identme": IdentMeProvider,
    "seeip": SeeIpProvider,
}

_DEFAULT_ORDER = ["ipify", "icanhazip", "identme", "seeip"]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="publicip",
        description="Report your internet-facing public IP address.",
    )
    parser.add_argument(
        "--provider",
        choices=list(_PROVIDERS.keys()),
        help="Use a specific provider instead of automatic fallback.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="all_providers",
        help="Query all providers and display each result.",
    )
    parser.add_argument(
        "--format",
        choices=["plain", "json"],
        default="plain",
        help="Output format (default: plain).",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Include the provider name in output.",
    )
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    formatter = JsonFormatter() if args.format == "json" else PlainFormatter()

    if args.all_providers:
        provider_instances = [cls() for cls in _PROVIDERS.values()]
        resolver = Resolver(provider_instances)
        results = resolver.resolve_all()
        for name, ip, error in results:
            if error:
                print(f"{name}: ERROR - {error}", file=sys.stderr)
            else:
                print(formatter.format(ip, name, verbose=True))
        return

    if args.provider:
        provider_instances = [_PROVIDERS[args.provider]()]
    else:
        provider_instances = [_PROVIDERS[k]() for k in _DEFAULT_ORDER]

    resolver = Resolver(provider_instances)
    try:
        ip, provider_name = resolver.resolve()
        print(formatter.format(ip, provider_name, verbose=args.verbose))
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
