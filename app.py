"""
Deep Research Agent — Gradio Web UI
Run with:  python app.py
"""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    import gradio as gr

    HAS_GRADIO = True
except ImportError:
    HAS_GRADIO = False

from graph.workflow import run_research
from tools.markdown import generate_markdown
from tools.pdf import markdown_to_pdf
from core.logger import logger


def process_query(query: str):
    """Run the full research pipeline and return results."""
    if not query or not query.strip():
        return "⚠️ Please enter a research query.", None, None

    logger.info(f"[Gradio] Starting research: {query}")

    try:
        report = run_research(query.strip())

        if not report:
            return "❌ Research pipeline did not produce a report.", None, None

        # Save to files
        md_path = generate_markdown(report)
        pdf_path = markdown_to_pdf(md_path)

        logger.info(f"[Gradio] Report saved: {md_path}, {pdf_path}")

        # Build markdown preview
        preview = f"# {report.title}\n\n"
        preview += f"## Executive Summary\n\n{report.executive_summary}\n\n"

        for section in report.sections:
            preview += f"## {section.heading}\n\n{section.content}\n\n"

        preview += "## References\n\n"
        for ref in report.references:
            preview += f"- [{ref}]({ref})\n"

        return preview, str(md_path), str(pdf_path)

    except Exception as e:
        logger.error(f"[Gradio] Research failed: {e}")
        return f"❌ Error: {e}", None, None


def create_app():
    """Build and return the Gradio interface."""
    if not HAS_GRADIO:
        print(
            "ERROR: Gradio is not installed.\n"
            "Install with:  pip install gradio\n"
        )
        return None

    with gr.Blocks(
        title="Deep Research Agent",
    ) as app:

        gr.Markdown(
            "# 🔬 Deep Research Agent\n"
            "Enter any research question. The agent will **plan → search → "
            "summarize → critique → refine → write** a professional report."
        )

        with gr.Row():
            with gr.Column(scale=3):
                query_input = gr.Textbox(
                    label="Research Query",
                    placeholder="e.g. Latest advancements in Small Language Models in 2026",
                    lines=3,
                )
                submit_btn = gr.Button(
                    "🚀 Generate Report",
                    variant="primary",
                    size="lg",
                )

            with gr.Column(scale=1):
                md_download = gr.File(label="📄 Markdown Report")
                pdf_download = gr.File(label="📕 PDF Report")

        gr.Markdown("---")
        output_preview = gr.Markdown(
            label="Report Preview",
            value="*Results will appear here after you click Generate Report…*",
        )

        submit_btn.click(
            fn=process_query,
            inputs=[query_input],
            outputs=[output_preview, md_download, pdf_download],
        )

    return app


if __name__ == "__main__":
    app = create_app()
    if app:
        app.launch(share=False, theme=gr.themes.Soft())
    else:
        print("Cannot launch application — Gradio is missing.")
