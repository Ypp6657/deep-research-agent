import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from core.llm import get_llm

llm = get_llm()

response = llm.invoke("Reply with exactly SUCCESS")

print(type(response))
print(response)
print(response.content)