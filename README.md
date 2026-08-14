# Document Portfolio Generator

Generate a consistent professional portfolio in Markdown, DOCX, and PDF from one validated JSON profile. The repository contains fictional example data and no personal CV, photograph, generated personal document, or inherited Git history.

## Why this project exists

Maintaining separate resume and portfolio files creates drift. This package keeps content in a portable JSON model and treats document formats as renderers. A single command creates reviewable Markdown, an editable Word document, and a shareable PDF.

## Features

- typed, validated profile loading;
- Markdown, DOCX, and PDF renderers;
- sections for contact details, skills, experience, projects, and education;
- safe URL-scheme validation for optional links;
- deterministic output names and explicit format selection;
- temporary-directory tests that inspect all three artifacts;
- no template-time network requests or hidden personal defaults.

The DOCX renderer uses the `compact_reference_guide` style system with a named `portfolio_one_page_density` override for concise portfolios: Letter pages and one-inch margins are retained while body and section spacing are tightened to prevent orphaned final sections.

## Run it

Python 3.11 or newer is required.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .

portfolio-docs \
  --input examples/profile.json \
  --output-dir generated
```

The output directory will contain:

```text
avery-morgan-portfolio.md
avery-morgan-portfolio.docx
avery-morgan-portfolio.pdf
```

Versioned GitHub Releases provide a wheel, source distribution, and SHA-256 checksums. Download a wheel from the [Releases page](https://github.com/MeherwerAli/document-portfolio-generator/releases), then install it with `python -m pip install ./document_portfolio_generator-<version>-py3-none-any.whl`.

Generate selected formats with `--formats markdown pdf`.

## Input model

The [fictional example profile](examples/profile.json) is the executable schema example. Required top-level fields are `name`, `headline`, `summary`, `contact`, `skills`, `experience`, `projects`, and `education`. Unknown fields are ignored so a source profile can evolve without breaking older renderers.

Links accept only `https`, `http`, and `mailto` schemes. Every renderer treats profile text as data, not markup.

## Verify it

```bash
python -m unittest discover --start-directory tests --verbose
python -m pip wheel --no-deps --wheel-dir dist .
```

The tests generate documents in a temporary directory. They verify the Markdown content, ZIP-based DOCX signature, PDF signature, output naming, format selection, and invalid-link rejection.

## Design boundary

This is a document-generation reference, not an applicant-tracking system or a claim-writing tool. It does not invent experience, scrape profile data, bundle personal assets, or upload generated documents.

## License

[MIT](LICENSE)
