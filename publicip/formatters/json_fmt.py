"""JSON formatter."""

import json

from publicip.formatters.base import OutputFormatter


class JsonFormatter(OutputFormatter):
    def format(self, ip: str, provider: str, verbose: bool) -> str:
        data: dict[str, str] = {"ip": ip}
        if verbose:
            data["provider"] = provider
        return json.dumps(data)
