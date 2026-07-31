from pathlib import Path
import os

from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
AGENTS_ROOT = Path(__file__).resolve().parents[3]

ENV_FILE = AGENTS_ROOT / ".env"

if not ENV_FILE.exists():
    raise FileNotFoundError(f".env not found at: {ENV_FILE}")

load_dotenv(ENV_FILE)

OUTPUT_DIR = PROJECT_ROOT / "outputs"
REPORTS_DIR = OUTPUT_DIR / "reports"
MARKDOWN_DIR = OUTPUT_DIR / "markdown"
HTML_DIR = OUTPUT_DIR / "html"
PDF_DIR = OUTPUT_DIR / "pdf"

# -----------------------------------------------------------------------------
# GPT-OSS Configuration
# -----------------------------------------------------------------------------

GPT_OSS_API_KEY = os.getenv("GPT_OSS_API_KEY")

GPT_OSS_BASE_URL = os.getenv(
    "GPT_OSS_BASE_URL",
    "https://apis.airawat.cdac.in/cdac-mtg/gpt120b/v1",
)

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "openai/gpt-oss-120b",
)

TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))

# -----------------------------------------------------------------------------
# Search
# -----------------------------------------------------------------------------

MAX_SEARCH_RESULTS = 5
MAX_RESEARCH_ITERATIONS = 3

# -----------------------------------------------------------------------------
# Create Output Directories
# -----------------------------------------------------------------------------

for directory in (
    OUTPUT_DIR,
    REPORTS_DIR,
    MARKDOWN_DIR,
    HTML_DIR,
    PDF_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)