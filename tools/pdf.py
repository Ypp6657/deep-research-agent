from pathlib import Path

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate

from config.settings import PDF_DIR


def markdown_to_pdf(markdown_path: Path) -> Path:
    """
    Convert a Markdown file into a simple PDF.
    """

    pdf_path = PDF_DIR / f"{markdown_path.stem}.pdf"

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(str(pdf_path))

    story = []

    text = markdown_path.read_text(encoding="utf-8")

    for line in text.splitlines():

        if not line.strip():
            continue

        story.append(
            Paragraph(line, styles["BodyText"])
        )

    doc.build(story)

    return pdf_path