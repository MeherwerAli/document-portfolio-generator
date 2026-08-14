from __future__ import annotations

import json
from pathlib import Path

from .models import Profile, ProfileValidationError


def load_profile(source: Path) -> Profile:
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ProfileValidationError(f"profile file does not exist: {source}") from error
    except json.JSONDecodeError as error:
        raise ProfileValidationError(
            f"profile file is not valid JSON at line {error.lineno}, column {error.colno}"
        ) from error
    return Profile.from_dict(data)
