from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate

from agents.base import BaseAgent
from core.schemas import SearchPlan
from config.settings import PROJECT_ROOT


class PlannerAgent(BaseAgent):

    def __init__(self):
        super().__init__()

        self.structured_llm = self.llm.with_structured_output(
            SearchPlan
            )

        prompt_text = (PROJECT_ROOT / "prompts" / "planner.md").read_text(
            encoding="utf-8"
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt_text),
                ("human", "{query}"),
            ]
        )

    def plan(self, query: str):

        chain = (
            self.prompt
            | self.structured_llm
        )

        return chain.invoke(
            {
                "query": query,
            }
        )