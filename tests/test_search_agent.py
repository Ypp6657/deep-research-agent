import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from agents.planner import PlannerAgent
from agents.search import SearchAgent


planner = PlannerAgent()

plan = planner.plan(
    "Latest advancements in Small Language Models in 2026"
)

agent = SearchAgent()

results = agent.search(plan)

print()

print(f"Tasks : {len(plan.tasks)}")

print(f"Results : {len(results)}")

print()

for r in results:

    print("=" * 80)

    print(r.title)

    print(r.url)

    print(r.content[:500])