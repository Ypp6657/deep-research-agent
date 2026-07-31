from datetime import datetime
from pathlib import Path

from config.settings import MARKDOWN_DIR
from core.schemas import FinalReport


def generate_markdown(report: FinalReport) -> Path:
    """
    Generate a Markdown report from a FinalReport object.
    """

    filename = (
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_report.md"
    )

    output_path = MARKDOWN_DIR / filename

    markdown = [
        f"# {report.title}",
        "",
        "## Executive Summary",
        "",
        report.executive_summary,
        "",
        "## Report",
        "",
    ]

    for section in report.sections:
        markdown.append(f"### {section.heading}")
        markdown.append("")
        markdown.append(section.content)
        markdown.append("")

    markdown.extend(
        [
            "## References",
            "",
        ]
    )

    for reference in report.references:
        markdown.append(f"- {reference}")

    output_path.write_text(
        "\n".join(markdown),
        encoding="utf-8",
    )

    return output_path