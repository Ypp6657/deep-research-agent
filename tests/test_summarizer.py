import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from agents.planner import PlannerAgent
from agents.search import SearchAgent
from agents.summarizer import SummarizerAgent


planner = PlannerAgent()

plan = planner.plan(
    "Latest advancements in Small Language Models in 2026"
)

search = SearchAgent()

results = search.search(plan)

summarizer = SummarizerAgent()

summaries = summarizer.summarize(results)

print()

print("=" * 100)

print(f"Generated {len(summaries)} summaries")

print("=" * 100)

for summary in summaries:

    print()

    print(summary.query)

    print()

    print(summary.summary)

    print()

    print(summary.key_points)

    print()

    print(summary.sources)

    print("=" * 100)