from __future__ import annotations

from .models import Profile


def render_markdown(profile: Profile) -> str:
    lines = [f"# {_escape(profile.name)}", "", f"**{_escape(profile.headline)}**"]
    if profile.location:
        lines.extend(["", _escape(profile.location)])

    lines.extend(["", _contact_line(profile), "", "## Profile", "", _escape(profile.summary)])
    lines.extend(["", "## Skills"])
    for section, values in profile.skills.items():
        lines.extend(["", f"**{_escape(section)}:** {', '.join(_escape(value) for value in values)}"])

    lines.extend(["", "## Experience"])
    for item in profile.experience:
        lines.extend([
            "",
            f"### {_escape(item.role)} — {_escape(item.organization)}",
            "",
            f"*{_escape(item.period)}*",
            "",
        ])
        lines.extend(f"- {_escape(highlight)}" for highlight in item.highlights)

    lines.extend(["", "## Projects"])
    for item in profile.projects:
        name = _link(item.name, item.url) if item.url else _escape(item.name)
        lines.extend([
            "",
            f"### {name}",
            "",
            _escape(item.summary),
            "",
            f"**Technologies:** {', '.join(_escape(value) for value in item.technologies)}",
        ])

    lines.extend(["", "## Education"])
    for item in profile.education:
        lines.extend([
            "",
            f"**{_escape(item.qualification)}**, {_escape(item.institution)} — {_escape(item.period)}",
        ])
    return "\n".join(lines).rstrip() + "\n"


def _contact_line(profile: Profile) -> str:
    items = []
    for item in profile.contact:
        value = _link(item.value, item.url) if item.url else _escape(item.value)
        items.append(f"**{_escape(item.label)}:** {value}")
    return " · ".join(items)


def _link(label: str, url: str) -> str:
    return f"[{_escape(label)}]({_escape_url(url)})"


def _escape(value: str) -> str:
    for character in "\\`*_{}[]<>#|":
        value = value.replace(character, f"\\{character}")
    return value


def _escape_url(value: str) -> str:
    return value.replace("(", "%28").replace(")", "%29")
