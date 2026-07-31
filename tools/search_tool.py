from typing import List

from ddgs import DDGS

from core.schemas import SearchResult


def search_web(query: str, max_results: int = 5) -> List[SearchResult]:
    """
    Search the web using DDGS (DuckDuckGo).
    """

    results = []

    with DDGS() as ddgs:
        for item in ddgs.text(query, max_results=max_results):
            results.append(
                SearchResult(
                    query=query,
                    objective="",
                    title=item.get("title", ""),
                    url=item.get("href", ""),
                    content=item.get("body", ""),
                )
            )

    return results