import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from core.llm import get_llm
from core.schemas import SearchSummary

llm = get_llm()

structured = llm.with_structured_output(SearchSummary)

response = structured.invoke(
    "Summarize Python in one sentence."
)

print(response)