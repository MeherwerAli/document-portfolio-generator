from __future__ import annotations

from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from .models import Profile


def write_pdf(profile: Profile, destination: Path) -> None:
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "PortfolioTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=23,
        leading=27,
        textColor=colors.HexColor("#0F2137"),
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "PortfolioSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#6B5224"),
        alignment=TA_CENTER,
        spaceAfter=8,
    )
    section_style = ParagraphStyle(
        "PortfolioSection",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#0F2137"),
        spaceBefore=9,
        spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "PortfolioBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=11,
        leading=13.75,
        textColor=colors.HexColor("#202630"),
        spaceAfter=4,
    )
    bullet_style = ParagraphStyle(
        "PortfolioBullet",
        parent=body_style,
        leftIndent=10,
        firstLineIndent=-7,
        bulletIndent=0,
    )

    document = SimpleDocTemplate(
        str(destination),
        pagesize=letter,
        rightMargin=25.4 * mm,
        leftMargin=25.4 * mm,
        topMargin=25.4 * mm,
        bottomMargin=25.4 * mm,
        title=profile.name,
        author=profile.name,
    )
    story = [
        Paragraph(escape(profile.name), title_style),
        Paragraph(escape(_subtitle(profile)), subtitle_style),
        Paragraph(escape(_contact_line(profile)), subtitle_style),
        Paragraph("PROFILE", section_style),
        Paragraph(escape(profile.summary), body_style),
        Paragraph("SKILLS", section_style),
    ]
    for section_name, values in profile.skills.items():
        story.append(Paragraph(
            f"<b>{escape(section_name)}:</b> {escape(', '.join(values))}",
            body_style,
        ))

    story.append(Paragraph("EXPERIENCE", section_style))
    for item in profile.experience:
        story.extend([
            Paragraph(
                f"<b>{escape(item.role)}</b> — {escape(item.organization)}",
                body_style,
            ),
            Paragraph(f"<i>{escape(item.period)}</i>", body_style),
        ])
        story.extend(
            Paragraph(f"• {escape(highlight)}", bullet_style)
            for highlight in item.highlights
        )

    story.append(Paragraph("PROJECTS", section_style))
    for item in profile.projects:
        story.extend([
            Paragraph(f"<b>{escape(item.name)}</b>", body_style),
            Paragraph(escape(item.summary), body_style),
            Paragraph(
                f"<b>Technologies:</b> {escape(', '.join(item.technologies))}",
                body_style,
            ),
        ])

    story.append(Paragraph("EDUCATION", section_style))
    for item in profile.education:
        story.append(Paragraph(
            f"<b>{escape(item.qualification)}</b>, {escape(item.institution)} — {escape(item.period)}",
            body_style,
        ))
    story.append(Spacer(1, 1))
    document.build(story)


def _subtitle(profile: Profile) -> str:
    return f"{profile.headline} · {profile.location}" if profile.location else profile.headline


def _contact_line(profile: Profile) -> str:
    return " · ".join(f"{item.label}: {item.value}" for item in profile.contact)
