import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from core.schemas import FinalReport, ReportSection
from tools.markdown import generate_markdown

report = FinalReport(
    title="AI Trends 2026",
    executive_summary="This report summarizes the latest AI trends.",
    sections=[
        ReportSection(
            heading="Foundation Models",
            content="Foundation models continue to evolve rapidly.",
        ),
        ReportSection(
            heading="Agentic AI",
            content="Agentic systems are becoming more capable.",
        ),
    ],
    references=[
        "https://openai.com",
        "https://ai.google",
    ],
)

path = generate_markdown(report)

print(f"Markdown saved to:\n{path}")