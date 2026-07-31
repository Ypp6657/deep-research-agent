import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from agents.planner import PlannerAgent
from agents.search import SearchAgent
from agents.summarizer import SummarizerAgent
from agents.critic import CriticAgent

query = """
Write a detailed report on Small Language Models in 2026.
"""

planner = PlannerAgent()
search = SearchAgent()
summarizer = SummarizerAgent()
critic = CriticAgent()

plan = planner.plan(query)

results = search.search(plan)

summaries = summarizer.summarize(results)

review = critic.review(
    user_query=query,
    summaries=summaries,
)

print("=" * 80)
print("CRITIC REVIEW")
print("=" * 80)

print(f"\nComplete: {review.is_complete}")

print("\nFeedback:")
print(review.overall_feedback)

print("\nStrengths:")
for s in review.strengths:
    print("-", s)

print("\nWeaknesses:")
for w in review.weaknesses:
    print("-", w)

print("\nAdditional Search Queries:")
for q in review.additional_search_queries:
    print("-", q)