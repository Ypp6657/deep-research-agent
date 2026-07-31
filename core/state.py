from typing import List, Optional

from typing_extensions import TypedDict

from core.schemas import (
    SearchTask,
    SearchResult,
    SearchSummary,
    CriticReview,
    FinalReport,
)


class ResearchState(TypedDict):
    user_query: str

    plan: List[SearchTask]

    search_results: List[SearchResult]

    summaries: List[SearchSummary]

    critic_review: Optional[CriticReview]

    final_report: Optional[FinalReport]

    iteration: int