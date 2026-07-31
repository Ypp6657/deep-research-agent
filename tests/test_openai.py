import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from openai import OpenAI
from pprint import pprint

from config.settings import *

client = OpenAI(
    api_key=GPT_OSS_API_KEY,
    base_url=GPT_OSS_BASE_URL,
)

response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly SUCCESS"
        }
    ],
    max_tokens=256,
)

print("=" * 80)
pprint(response.model_dump())
print("=" * 80)

print("\nCONTENT:")
print(response.choices[0].message.content)

# Note: reasoning field may be present for reasoning models
reasoning = getattr(response.choices[0].message, 'reasoning', None)
if reasoning:
    print("\nREASONING:")
    print(reasoning)