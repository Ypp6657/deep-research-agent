from typing import List, Optional

from pydantic import BaseModel, Field


class SearchTask(BaseModel):
    query: str
    objective: str
    priority: int = Field(default=1)

class SearchPlan(BaseModel):
    tasks: List[SearchTask]

class SearchResult(BaseModel):
    query: str
    objective: str
    title: str
    url: str
    content: str


class SearchSummary(BaseModel):
    query: str
    objective: str
    summary: str
    key_points: List[str]
    sources: List[str] = Field(default_factory=list)


class CriticReview(BaseModel):
    is_complete: bool

    overall_feedback: str

    additional_search_queries: List[str] = Field(default_factory=list)

    strengths: List[str] = Field(default_factory=list)

    weaknesses: List[str] = Field(default_factory=list)


class ReportSection(BaseModel):
    heading: str
    content: str


class FinalReport(BaseModel):
    title: str
    executive_summary: str
    sections: List[ReportSection]
    references: List[str]


