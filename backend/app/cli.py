"""Command-line interface: python -m app.cli <url> [--lang ar|en] [--json]"""

from __future__ import annotations

import argparse
import json
import sys

from .core.analyzer import InvalidUrlError, analyze_url
from .core.messages import ERRORS, VERDICT_ADVICE, VERDICT_LABELS

COLORS = {"safe": "\033[32m", "suspicious": "\033[33m", "dangerous": "\033[31m"}
SEVERITY_COLORS = {"high": "\033[31m", "medium": "\033[33m", "low": "\033[36m"}
RESET = "\033[0m"
EXIT_CODES = {"safe": 0, "suspicious": 1, "dangerous": 2}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phishing URL Detector")
    parser.add_argument("url", help="URL to analyze")
    parser.add_argument("--lang", choices=("ar", "en"), default="ar")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    parser.add_argument("--no-color", action="store_true")
    args = parser.parse_args(argv)

    try:
        result = analyze_url(args.url)
    except InvalidUrlError as exc:
        print(ERRORS[exc.code][args.lang], file=sys.stderr)
        return 3

    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
        return EXIT_CODES[result.verdict]

    use_color = sys.stdout.isatty() and not args.no_color

    def paint(text: str, color: str) -> str:
        return f"{color}{text}{RESET}" if use_color else text

    lang = args.lang
    label = VERDICT_LABELS[result.verdict][lang]
    print(paint(f"{label}  ({result.score}/100)", COLORS[result.verdict]))
    print(result.normalized_url)
    print(VERDICT_ADVICE[result.verdict][lang])
    for f in result.findings:
        print(f"  {paint('●', SEVERITY_COLORS[f.severity])} {f.title[lang]}: {f.detail[lang]}")
    return EXIT_CODES[result.verdict]


if __name__ == "__main__":
    sys.exit(main())
