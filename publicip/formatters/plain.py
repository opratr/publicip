"""Plain text formatter."""

from publicip.formatters.base import OutputFormatter


class PlainFormatter(OutputFormatter):
    def format(self, ip: str, provider: str, verbose: bool) -> str:
        if verbose:
            return f"{ip}\t(via {provider})"
        return ip
