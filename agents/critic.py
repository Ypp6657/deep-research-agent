from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate

from agents.base import BaseAgent
from config.settings import PROJECT_ROOT

from core.schemas import (
    SearchSummary,
    CriticReview,
)


class CriticAgent(BaseAgent):

    def __init__(self):
        super().__init__()

        self.structured_llm = (
            self.llm.with_structured_output(
                CriticReview
            )
        )

        prompt_text = (PROJECT_ROOT / "prompts" / "critic.md").read_text(
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

    def review(
        self,
        user_query: str,
        summaries: list[SearchSummary],
    ) -> CriticReview:

        summaries_text = ""

        for summary in summaries:

            summaries_text += (
                f"\n"
                f"Query: {summary.query}\n"
                f"Objective: {summary.objective}\n\n"
                f"Summary:\n"
                f"{summary.summary}\n\n"
                f"Key Points:\n"
            )

            for point in summary.key_points:
                summaries_text += f"- {point}\n"

            summaries_text += "\nSources:\n"

            for src in summary.sources:
                summaries_text += f"- {src}\n"

            summaries_text += "\n" + "=" * 80 + "\n\n"

        chain = (
            self.prompt
            | self.structured_llm
        )

        review = chain.invoke(
            {
                "user_query": user_query,
                "summaries": summaries_text,
            }
        )

        return review