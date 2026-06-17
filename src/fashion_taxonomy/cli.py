"""Command-line interface for the Fashion Taxonomy analyzer.

Examples:
    fashion-taxonomy analyze dress.jpg
    fashion-taxonomy analyze dress.jpg --provider gemini --json -o result.json
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from fashion_taxonomy import __version__
from fashion_taxonomy.analyzer import FashionAnalyzer
from fashion_taxonomy.config import get_settings
from fashion_taxonomy.exceptions import FashionTaxonomyError
from fashion_taxonomy.logging_config import configure_logging
from fashion_taxonomy.models import ImageInput
from fashion_taxonomy.rendering import to_text


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fashion-taxonomy",
        description="Analyze a fashion image into a structured taxonomy.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    analyze = sub.add_parser("analyze", help="Analyze a single image.")
    analyze.add_argument("image", type=Path, help="Path to a JPG/PNG/WEBP image.")
    analyze.add_argument(
        "--provider",
        choices=["openai", "gemini"],
        help="Override the provider configured in .env.",
    )
    analyze.add_argument("--json", action="store_true", help="Output JSON instead of text.")
    analyze.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Write the result to this file (in addition to stdout).",
    )
    return parser


def _run_analyze(args: argparse.Namespace) -> int:
    settings = get_settings()
    configure_logging(settings.log_level)
    analyzer = FashionAnalyzer(settings)

    image = ImageInput.from_path(args.image)
    taxonomy = analyzer.analyze(image, provider=args.provider)

    output = (
        taxonomy.model_dump_json(indent=2) if args.json else to_text(taxonomy)
    )
    print(output)
    if args.output:
        args.output.write_text(output, encoding="utf-8")
        print(f"\nSaved to {args.output}", file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    """CLI entry point. Returns a process exit code."""
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "analyze":
            return _run_analyze(args)
    except FashionTaxonomyError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:  # pragma: no cover
        print("\nInterrupted.", file=sys.stderr)
        return 130
    return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
