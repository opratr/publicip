# publicip

[![CI](https://github.com/opratr/publicip/actions/workflows/ci.yml/badge.svg)](https://github.com/opratr/publicip/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/publicip)](https://pypi.org/project/publicip/)
[![Python versions](https://img.shields.io/pypi/pyversions/publicip)](https://pypi.org/project/publicip/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A command-line utility that reports your internet-facing public IP address. Queries multiple well-known free services with automatic fallback so you always get an answer even if a provider is down.

## Installation

```bash
pip install publicip
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv tool install publicip
```

## Usage

```
publicip                        # print your public IP
publicip --verbose              # include which provider responded
publicip --format json          # JSON output
publicip --format json --verbose  # JSON with provider field
publicip --provider ipify       # force a specific provider
publicip --all                  # query all providers
```

### Providers

| Name        | Service            |
|-------------|--------------------|
| `ipify`     | api.ipify.org      |
| `icanhazip` | icanhazip.com      |
| `identme`   | api.ident.me       |
| `seeip`     | ip4.seeip.org      |

The default order is `ipify → icanhazip → identme → seeip`. The first successful response wins.

### Examples

```bash
$ publicip
203.0.113.42

$ publicip --verbose
203.0.113.42    (via ipify)

$ publicip --format json --verbose
{"ip": "203.0.113.42", "provider": "ipify"}

$ publicip --all
203.0.113.42    (via ipify)
203.0.113.42    (via icanhazip)
203.0.113.42    (via ident.me)
203.0.113.42    (via seeip)
```

## Limitations

Currently, `publicip` only returns your public **IPv4** address. IPv6 is not supported. All configured providers are queried via their IPv4 endpoints.

IPv6 support is a planned future enhancement.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

To report a vulnerability privately, see [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE) © Andre Van Klaveren
