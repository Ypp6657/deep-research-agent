from tools.utils import (
    normalize_text,
    safe_filename,
    utc_timestamp,
    is_valid_url,
    truncate_text,
)

print(normalize_text("Hello    \n\n   World"))
print(safe_filename("AI Report: 2026/07?"))
print(utc_timestamp())
print(is_valid_url("https://openai.com"))
print(is_valid_url("abc"))
print(truncate_text("A" * 20, 10))