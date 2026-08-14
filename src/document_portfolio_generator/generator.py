from __future__ import annotations

import re
from pathlib import Path

from .models import Profile
from .render_docx import write_docx
from .render_markdown import render_markdown
from .render_pdf import write_pdf


SUPPORTED_FORMATS = ("markdown", "docx", "pdf")


def generate_portfolio(
    profile: Profile,
    output_dir: Path,
    formats: tuple[str, ...] = SUPPORTED_FORMATS,
) -> list[Path]:
    unknown_formats = sorted(set(formats) - set(SUPPORTED_FORMATS))
    if unknown_formats:
        raise ValueError(f"unsupported formats: {', '.join(unknown_formats)}")
    if not formats:
        raise ValueError("at least one output format is required")

    output_dir.mkdir(parents=True, exist_ok=True)
    base_name = f"{_slug(profile.name)}-portfolio"
    outputs: list[Path] = []
    for output_format in formats:
        suffix = "md" if output_format == "markdown" else output_format
        destination = output_dir / f"{base_name}.{suffix}"
        if output_format == "markdown":
            destination.write_text(render_markdown(profile), encoding="utf-8")
        elif output_format == "docx":
            write_docx(profile, destination)
        else:
            write_pdf(profile, destination)
        outputs.append(destination)
    return outputs


def _slug(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return normalized or "portfolio"
