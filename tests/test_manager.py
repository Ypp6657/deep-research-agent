import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from agents.manager import ResearchManager


query = """
Write a detailed report on Small Language Models in 2026.
"""


manager = ResearchManager()

report, is_complete = manager.run(query)


print("\n")
print("=" * 100)
print("Research Complete:", is_complete)
print("=" * 100)

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