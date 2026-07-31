from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
import re


def normalize_text(text: str) -> str:
    """
    Remove excessive whitespace from text.
    """
    return re.sub(r"\s+", " ", text).strip()


def safe_filename(name: str, max_length: int = 100) -> str:
    """
    Convert arbitrary text into a filesystem-safe filename.
    """
    name = re.sub(r'[<>:"/\\|?*]', "", name)
    name = re.sub(r"\s+", "_", name.strip())

    return name[:max_length]


def utc_timestamp() -> str:
    """
    Return current UTC timestamp.
    """
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def is_valid_url(url: str) -> bool:
    """
    Validate an HTTP/HTTPS URL.
    """
    try:
        parsed = urlparse(url)
        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
        )
    except Exception:
        return False


def truncate_text(text: str, max_chars: int = 12000) -> str:
    """
    Truncate text before sending it to the LLM.
    """
    if len(text) <= max_chars:
        return text

    return text[:max_chars]