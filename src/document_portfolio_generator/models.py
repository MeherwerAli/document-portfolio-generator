from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from urllib.parse import urlsplit


class ProfileValidationError(ValueError):
    pass


@dataclass(frozen=True)
class ContactItem:
    label: str
    value: str
    url: str = ""


@dataclass(frozen=True)
class ExperienceItem:
    role: str
    organization: str
    period: str
    highlights: list[str]


@dataclass(frozen=True)
class ProjectItem:
    name: str
    summary: str
    technologies: list[str]
    url: str = ""


@dataclass(frozen=True)
class EducationItem:
    qualification: str
    institution: str
    period: str


@dataclass(frozen=True)
class Profile:
    name: str
    headline: str
    location: str
    summary: str
    contact: list[ContactItem]
    skills: dict[str, list[str]]
    experience: list[ExperienceItem]
    projects: list[ProjectItem]
    education: list[EducationItem]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Profile:
        if not isinstance(data, dict):
            raise ProfileValidationError("profile root must be a JSON object")

        contact = [
            ContactItem(
                label=_required_text(item, "label", "contact item"),
                value=_required_text(item, "value", "contact item"),
                url=_optional_url(item.get("url", ""), "contact item url"),
            )
            for item in _object_list(data, "contact")
        ]
        skills_value = data.get("skills")
        if not isinstance(skills_value, dict) or not skills_value:
            raise ProfileValidationError("skills must be a non-empty object")
        skills = {
            _clean_text(section, "skill section name"): _text_list(values, f"skills.{section}")
            for section, values in skills_value.items()
        }
        experience = [
            ExperienceItem(
                role=_required_text(item, "role", "experience item"),
                organization=_required_text(item, "organization", "experience item"),
                period=_required_text(item, "period", "experience item"),
                highlights=_text_list(item.get("highlights"), "experience highlights"),
            )
            for item in _object_list(data, "experience")
        ]
        projects = [
            ProjectItem(
                name=_required_text(item, "name", "project item"),
                summary=_required_text(item, "summary", "project item"),
                technologies=_text_list(item.get("technologies"), "project technologies"),
                url=_optional_url(item.get("url", ""), "project url"),
            )
            for item in _object_list(data, "projects")
        ]
        education = [
            EducationItem(
                qualification=_required_text(item, "qualification", "education item"),
                institution=_required_text(item, "institution", "education item"),
                period=_required_text(item, "period", "education item"),
            )
            for item in _object_list(data, "education")
        ]

        return cls(
            name=_required_text(data, "name", "profile"),
            headline=_required_text(data, "headline", "profile"),
            location=_optional_text(data.get("location", ""), "location"),
            summary=_required_text(data, "summary", "profile"),
            contact=contact,
            skills=skills,
            experience=experience,
            projects=projects,
            education=education,
        )


def _object_list(data: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        raise ProfileValidationError(f"{key} must be a non-empty array")
    if not all(isinstance(item, dict) for item in value):
        raise ProfileValidationError(f"{key} entries must be objects")
    return value


def _text_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ProfileValidationError(f"{label} must be a non-empty array")
    return [_clean_text(item, label) for item in value]


def _required_text(data: dict[str, Any], key: str, label: str) -> str:
    if key not in data:
        raise ProfileValidationError(f"{label} is missing {key}")
    return _clean_text(data[key], f"{label}.{key}")


def _optional_text(value: Any, label: str) -> str:
    if value == "":
        return ""
    return _clean_text(value, label)


def _clean_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProfileValidationError(f"{label} must be a non-empty string")
    return " ".join(value.split())


def _optional_url(value: Any, label: str) -> str:
    if value == "":
        return ""
    normalized = _clean_text(value, label)
    parsed = urlsplit(normalized)
    if parsed.scheme.lower() not in {"http", "https", "mailto"}:
        raise ProfileValidationError(f"{label} must use http, https, or mailto")
    if parsed.scheme.lower() in {"http", "https"} and not parsed.hostname:
        raise ProfileValidationError(f"{label} must contain a hostname")
    return normalized
