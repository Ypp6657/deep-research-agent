import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from tools.search_tool import search_web

results = search_web("Latest AI trends 2026", max_results=3)

print(f"Found {len(results)} results\n")

for i, result in enumerate(results, start=1):
    print("=" * 80)
    print(result.title)
    print(result.url)
    print(result.content)