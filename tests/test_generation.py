from __future__ import annotations

import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from document_portfolio_generator import generate_portfolio, load_profile
from document_portfolio_generator.models import Profile, ProfileValidationError


ROOT = Path(__file__).resolve().parents[1]


class PortfolioGenerationTest(unittest.TestCase):
    def test_generates_markdown_docx_and_pdf_from_fixture(self) -> None:
        profile = load_profile(ROOT / "examples" / "profile.json")

        with tempfile.TemporaryDirectory() as temporary_directory:
            outputs = generate_portfolio(profile, Path(temporary_directory))
            self.assertEqual(
                [
                    "avery-morgan-portfolio.md",
                    "avery-morgan-portfolio.docx",
                    "avery-morgan-portfolio.pdf",
                ],
                [output.name for output in outputs],
            )
            markdown, docx, pdf = outputs
            self.assertIn("# Avery Morgan", markdown.read_text(encoding="utf-8"))
            self.assertTrue(zipfile.is_zipfile(docx))
            self.assertEqual(b"%PDF", pdf.read_bytes()[:4])
            self.assertGreater(pdf.stat().st_size, 1_000)

    def test_generates_only_requested_formats(self) -> None:
        profile = load_profile(ROOT / "examples" / "profile.json")

        with tempfile.TemporaryDirectory() as temporary_directory:
            outputs = generate_portfolio(
                profile,
                Path(temporary_directory),
                ("markdown",),
            )
            self.assertEqual(["avery-morgan-portfolio.md"], [output.name for output in outputs])

    def test_rejects_unsafe_link_scheme(self) -> None:
        data = json.loads((ROOT / "examples" / "profile.json").read_text(encoding="utf-8"))
        data["projects"][0]["url"] = "javascript:alert(1)"

        with self.assertRaisesRegex(ProfileValidationError, "http, https, or mailto"):
            Profile.from_dict(data)

    def test_rejects_missing_required_section(self) -> None:
        data = json.loads((ROOT / "examples" / "profile.json").read_text(encoding="utf-8"))
        del data["experience"]

        with self.assertRaisesRegex(ProfileValidationError, "experience"):
            Profile.from_dict(data)


if __name__ == "__main__":
    unittest.main()
