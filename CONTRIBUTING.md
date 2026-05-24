# Contributing to publicip

Thank you for your interest in contributing! Please read this guide before submitting changes.

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) for dependency management

### Setup

```bash
git clone https://github.com/opratr/publicip.git
cd publicip
uv sync --frozen
```

### Running Tests

```bash
uv run pytest
```

### Linting and Type Checking

```bash
uv run ruff check .
uv run mypy publicip
```

### Security Checks

```bash
uv run bandit -lll -r publicip
uv run pip-audit
```

## Submitting Changes

1. Fork the repository and create a feature branch from `main`.
2. Write tests for any new behavior.
3. Ensure all CI checks pass locally before opening a PR.
4. Update `CHANGELOG.md` under `[Unreleased]`.
5. Open a pull request - fill out the template completely.

## Adding a New Provider

1. Create `publicip/providers/<name>.py` subclassing `IPProvider`.
2. Register it in `publicip/providers/__init__.py` and `publicip/cli.py`.
3. Add corresponding tests in `tests/test_providers.py`.

## Code Style

- Formatted with [ruff](https://docs.astral.sh/ruff/).
- Fully typed: `mypy --strict` must pass.
- No comments unless the *why* is non-obvious.

## Reporting Bugs

Open a GitHub issue using the bug report template.

## Security Vulnerabilities

See [SECURITY.md](SECURITY.md) for the private disclosure process.
