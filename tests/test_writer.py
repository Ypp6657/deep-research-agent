import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from agents.planner import PlannerAgent
from agents.search import SearchAgent
from agents.summarizer import SummarizerAgent
from agents.critic import CriticAgent
from agents.writer import WriterAgent

query = """
Write a detailed report on Small Language Models in 2026.
"""

planner = PlannerAgent()
search = SearchAgent()
summarizer = SummarizerAgent()
critic = CriticAgent()
writer = WriterAgent()

plan = planner.plan(query)

results = search.search(plan)

summaries = summarizer.summarize(results)

review = critic.review(
    query,
    summaries,
)

print("\nResearch Complete:", review.is_complete)

report = writer.write(
    query,
    summaries,
)

print("\n")
print("=" * 100)
print(report.title)
print("=" * 100)

print("\nExecutive Summary\n")
print(report.executive_summary)

for section in report.sections:

    print("\n")
    print("#", section.heading)
    print(section.content)

print("\nReferences")

for ref in report.references:
    print("-", ref)