from agents.base import BaseAgent
from tools.utils import truncate_text

from core.schemas import (
    SearchPlan,
    SearchResult,
)

from tools.search_tool import search_web
from tools.browser import fetch_page


class SearchAgent(BaseAgent):

    def __init__(
        self,
        max_results: int = 3,
    ):
        super().__init__()
        self.max_results = max_results

    def search(
        self,
        plan: SearchPlan,
    ) -> list[SearchResult]:

        all_results = []

        for task in plan.tasks:

            self.logger.info(
                f"Searching: {task.query}"
            )

            urls = search_web(
                query=task.query,
                max_results=self.max_results,
            )

            for item in urls:

                try:

                    content = truncate_text(
                        fetch_page(
                            item.url
                        )
                    )

                    result = SearchResult(
                        query=task.query,
                        objective=task.objective,
                        title=item.title,
                        url=item.url,
                        content=content,
                    )

                    all_results.append(result)

                except Exception as e:

                    self.logger.warning(
                        f"Failed: {item.url} :: {e}"
                    )

        return all_results

    def search_queries(
        self,
        queries: list[str],
    ) -> list[SearchResult]:

        all_results = []

        for query in queries:

            self.logger.info(
                f"Searching: {query}"
            )

            urls = search_web(
                query=query,
                max_results=self.max_results,
            )

            for item in urls:

                try:

                    content = truncate_text(
                        fetch_page(
                            item.url
                        )
                    )

                    result = SearchResult(
                        query=query,
                        objective="Additional research requested by Critic",
                        title=item.title,
                        url=item.url,
                        content=content,
                    )

                    all_results.append(result)

                except Exception as e:

                    self.logger.warning(
                        f"Failed: {item.url} :: {e}"
                    )

        return all_results