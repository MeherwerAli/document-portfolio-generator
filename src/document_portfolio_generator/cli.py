from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .generator import SUPPORTED_FORMATS, generate_portfolio
from .loader import load_profile
from .models import ProfileValidationError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate Markdown, DOCX, and PDF portfolio documents from JSON data.",
    )
    parser.add_argument("--input", type=Path, required=True, help="JSON profile path")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--formats",
        nargs="+",
        choices=SUPPORTED_FORMATS,
        default=list(SUPPORTED_FORMATS),
    )
    return parser


def main(arguments: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(arguments)
    try:
        profile = load_profile(args.input)
        outputs = generate_portfolio(profile, args.output_dir, tuple(args.formats))
    except (ProfileValidationError, ValueError) as error:
        raise SystemExit(str(error)) from error
    for output in outputs:
        print(output)
    return 0
