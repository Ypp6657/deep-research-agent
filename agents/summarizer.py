from pathlib import Path
from tools.utils import truncate_text
from collections import defaultdict

from langchain_core.prompts import ChatPromptTemplate

from agents.base import BaseAgent
from config.settings import PROJECT_ROOT

from core.schemas import (
    SearchResult,
    SearchSummary,
)


class SummarizerAgent(BaseAgent):

    MAX_RETRIES = 2

    def __init__(self):
        super().__init__()

        self.structured_llm = (
            self.llm.with_structured_output(
                SearchSummary
            )
        )

        prompt_text = (PROJECT_ROOT / "prompts" / "summarizer.md").read_text(
            encoding="utf-8"
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt_text),
                (
                    "human",
                    """
Research Task:
{query}

Objective:
{objective}

Search Results:

{documents}
                    """,
                ),
            ]
        )

    def _invoke_with_retry(self, chain, inputs: dict, label: str) -> SearchSummary:
        """Invoke the chain with retry logic for truncated JSON errors."""
        last_error = None
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                return chain.invoke(inputs)
            except Exception as e:
                last_error = e
                self.logger.warning(
                    f"Summarization attempt {attempt}/{self.MAX_RETRIES} "
                    f"failed for '{label}': {e}"
                )
                # On retry, reduce document size to give LLM more room
                if "documents" in inputs:
                    current = inputs["documents"]
                    inputs["documents"] = truncate_text(
                        current, max_chars=len(current) // 2
                    )

        # All retries exhausted — return a fallback summary
        self.logger.error(
            f"All {self.MAX_RETRIES} attempts failed for '{label}'. "
            f"Returning fallback summary. Last error: {last_error}"
        )
        return SearchSummary(
            query=inputs.get("query", label),
            objective=inputs.get("objective", ""),
            summary=f"Summarization failed after {self.MAX_RETRIES} attempts.",
            key_points=["Summarization error — content may have been too large."],
            sources=[],
        )

    def summarize(
        self,
        results: list[SearchResult],
    ) -> list[SearchSummary]:

        grouped = defaultdict(list)

        for result in results:
            grouped[result.query].append(result)

        summaries = []

        for query, docs in grouped.items():

            objective = getattr(
                docs[0],
                "objective",
                "",
            )

            sources = []

            text = ""

            for doc in docs:

                sources.append(doc.url)

                text += (
                    f"\nTitle: {doc.title}\n"
                    f"URL: {doc.url}\n"
                    f"Content:{truncate_text(doc.content, max_chars=2000)}\n\n"
                )

            chain = (
                self.prompt
                | self.structured_llm
            )

            summary = self._invoke_with_retry(
                chain,
                {
                    "query": query,
                    "objective": objective,
                    "documents": text,
                },
                label=query,
            )

            summary.sources = sources

            summaries.append(summary)

        return summaries