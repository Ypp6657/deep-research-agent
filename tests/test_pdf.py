import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from tools.markdown import generate_markdown
from tools.pdf import markdown_to_pdf
from core.schemas import FinalReport, ReportSection

report = FinalReport(
    title="AI Trends 2026",
    executive_summary="Summary",
    sections=[
        ReportSection(heading="Introduction", content="This is a report."),
    ],
    references=[
        "https://openai.com",
    ],
)

md = generate_markdown(report)
pdf = markdown_to_pdf(md)

print(pdf)