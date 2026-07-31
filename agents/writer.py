from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate

from agents.base import BaseAgent
from config.settings import PROJECT_ROOT
from tools.utils import truncate_text

from core.schemas import (
    SearchSummary,
    FinalReport,
    ReportSection,
)


class WriterAgent(BaseAgent):

    MAX_RETRIES = 2

    def __init__(self):
        super().__init__()

        self.structured_llm = (
            self.llm.with_structured_output(
                FinalReport
            )
        )

        prompt_text = (PROJECT_ROOT / "prompts" / "writer.md").read_text(
            encoding="utf-8"
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt_text),
                (
                    "human",
                    """
Original User Query:

{user_query}

Research Summaries:

{summaries}
                    """,
                ),
            ]
        )

    def write(
        self,
        user_query: str,
        summaries: list[SearchSummary],
    ) -> FinalReport:

        summaries_text = ""

        references = []

        for summary in summaries:

            summaries_text += (
                f"\n"
                f"Query: {summary.query}\n"
                f"Objective: {summary.objective}\n\n"
                f"{summary.summary}\n\n"
            )

            references.extend(summary.sources)

        chain = (
            self.prompt
            | self.structured_llm
        )

        inputs = {
            "user_query": user_query,
            "summaries": summaries_text,
        }

        last_error = None
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                report = chain.invoke(inputs)
                report.references = sorted(set(references))
                return report
            except Exception as e:
                last_error = e
                self.logger.warning(
                    f"Writer attempt {attempt}/{self.MAX_RETRIES} failed: {e}"
                )
                # Shrink input on retry
                inputs["summaries"] = truncate_text(
                    inputs["summaries"],
                    max_chars=len(inputs["summaries"]) // 2,
                )

        self.logger.error(f"Writer failed after {self.MAX_RETRIES} attempts: {last_error}")
        return FinalReport(
            title="Research Report (partial)",
            executive_summary="Report generation encountered an error. Partial data below.",
            sections=[
                ReportSection(
                    heading="Error",
                    content=f"The report writer failed: {last_error}",
                )
            ],
            references=sorted(set(references)),
        )