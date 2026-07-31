import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from agents.planner import PlannerAgent

planner = PlannerAgent()

plan = planner.plan(
    "Latest advancements in Small Language Models in 2026"
)

print(plan)