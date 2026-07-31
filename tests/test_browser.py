import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from tools.browser import fetch_page

url = "https://en.wikipedia.org/wiki/Large_language_model"

text = fetch_page(url)

print(f"Characters: {len(text)}")
print()
print(text[:1000])