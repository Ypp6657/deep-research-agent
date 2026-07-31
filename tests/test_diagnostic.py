"""
Comprehensive diagnostic test for the deep research pipeline.
Tests each component in isolation, then integration.
"""
import sys
import os

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

print("=" * 80)
print("DEEP RESEARCH AGENT - DIAGNOSTIC TEST")
print("=" * 80)

# ─────────────────────────────────────────────────
# TEST 1: Settings & env loading
# ─────────────────────────────────────────────────
print("\n[TEST 1] Settings & Environment")
try:
    from config.settings import (
        GPT_OSS_API_KEY, GPT_OSS_BASE_URL, MODEL_NAME,
        TEMPERATURE, MAX_TOKENS, PROJECT_ROOT, AGENTS_ROOT
    )
    assert GPT_OSS_API_KEY, "GPT_OSS_API_KEY is empty!"
    assert GPT_OSS_BASE_URL, "GPT_OSS_BASE_URL is empty!"
    print(f"  MODEL     : {MODEL_NAME}")
    print(f"  BASE_URL  : {GPT_OSS_BASE_URL}")
    print(f"  TEMP      : {TEMPERATURE}")
    print(f"  MAX_TOKENS: {MAX_TOKENS}")
    print(f"  PROJECT   : {PROJECT_ROOT}")
    print(f"  AGENTS    : {AGENTS_ROOT}")
    print("  [PASS]")
except Exception as e:
    print(f"  [FAIL] {e}")
    sys.exit(1)

# ─────────────────────────────────────────────────
# TEST 2: Schemas
# ─────────────────────────────────────────────────
print("\n[TEST 2] Pydantic Schemas")
try:
    from core.schemas import (
        SearchTask, SearchPlan, SearchResult,
        SearchSummary, CriticReview, ReportSection, FinalReport,
    )
    # Test creating instances
    task = SearchTask(query="test", objective="test obj", priority=1)
    plan = SearchPlan(tasks=[task])
    result = SearchResult(query="q", objective="o", title="t", url="http://x.com", content="c")
    summary = SearchSummary(query="q", objective="o", summary="s", key_points=["kp1"])
    review = CriticReview(is_complete=True, overall_feedback="good")
    section = ReportSection(heading="H", content="C")
    report = FinalReport(
        title="T", executive_summary="ES",
        sections=[section], references=["ref1"]
    )
    print(f"  All schemas created OK")
    print(f"  ReportSection: heading={section.heading}, content={section.content}")
    print("  [PASS]")
except Exception as e:
    print(f"  [FAIL] {e}")

# ─────────────────────────────────────────────────
# TEST 3: Utils
# ─────────────────────────────────────────────────
print("\n[TEST 3] Utility Functions")
try:
    from tools.utils import normalize_text, safe_filename, utc_timestamp, is_valid_url, truncate_text
    assert normalize_text("  hello   world  ") == "hello world"
    assert safe_filename('AI Report: 2026/07?') == "AI_Report_202607"
    assert len(utc_timestamp()) > 0
    assert is_valid_url("https://openai.com") == True
    assert is_valid_url("not-a-url") == False
    assert truncate_text("A" * 20, 10) == "A" * 10
    print("  [PASS]")
except Exception as e:
    print(f"  [FAIL] {e}")

# ─────────────────────────────────────────────────
# TEST 4: DuckDuckGo Search
# ─────────────────────────────────────────────────
print("\n[TEST 4] DuckDuckGo Search")
try:
    from tools.search_tool import search_web
    results = search_web("Python programming language", max_results=2)
    assert len(results) > 0, "No search results returned"
    for r in results:
        print(f"  - {r.title[:60]}... ({r.url[:50]})")
    print("  [PASS]")
except Exception as e:
    print(f"  [FAIL] {e}")

# ─────────────────────────────────────────────────
# TEST 5: Browser/Fetch
# ─────────────────────────────────────────────────
print("\n[TEST 5] Browser Fetch")
try:
    from tools.browser import fetch_page
    text = fetch_page("https://httpbin.org/html")
    assert len(text) > 50, f"Too short: {len(text)} chars"
    print(f"  Fetched {len(text)} chars")
    print("  [PASS]")
except Exception as e:
    print(f"  [FAIL] {e}")

# ─────────────────────────────────────────────────
# TEST 6: LLM Basic Invocation
# ─────────────────────────────────────────────────
print("\n[TEST 6] LLM Basic Invocation")
try:
    from core.llm import get_llm
    llm = get_llm()
    response = llm.invoke("Reply with exactly: SUCCESS")
    print(f"  Response type: {type(response).__name__}")
    print(f"  Content: {repr(response.content)}")
    assert response.content, f"content is empty/None! Response: {response}"
    print("  [PASS]")
except Exception as e:
    print(f"  [FAIL] {e}")

# ─────────────────────────────────────────────────
# TEST 7: LLM Structured Output (SearchPlan)
# ─────────────────────────────────────────────────
print("\n[TEST 7] LLM Structured Output - SearchPlan")
try:
    from core.llm import get_llm
    from core.schemas import SearchPlan
    llm = get_llm()
    structured = llm.with_structured_output(SearchPlan)
    result = structured.invoke(
        "Create a research plan with 2 tasks about Python programming."
    )
    print(f"  Result type: {type(result).__name__}")
    print(f"  Tasks: {len(result.tasks)}")
    for t in result.tasks:
        print(f"    - [{t.priority}] {t.query} | {t.objective}")
    print("  [PASS]")
except Exception as e:
    print(f"  [FAIL] {e}")

# ─────────────────────────────────────────────────
# TEST 8: LLM Structured Output (SearchSummary)
# ─────────────────────────────────────────────────
print("\n[TEST 8] LLM Structured Output - SearchSummary")
try:
    from core.llm import get_llm
    from core.schemas import SearchSummary
    llm = get_llm()
    structured = llm.with_structured_output(SearchSummary)
    result = structured.invoke("Summarize Python programming in one sentence.")
    print(f"  Summary: {result.summary[:100]}...")
    print(f"  Key points: {len(result.key_points)}")
    print("  [PASS]")
except Exception as e:
    print(f"  [FAIL] {e}")

# ─────────────────────────────────────────────────
# TEST 9: LLM Structured Output (CriticReview)
# ─────────────────────────────────────────────────
print("\n[TEST 9] LLM Structured Output - CriticReview")
try:
    from core.llm import get_llm
    from core.schemas import CriticReview
    llm = get_llm()
    structured = llm.with_structured_output(CriticReview)
    result = structured.invoke(
        "Review this research: Python is a popular language. Is this complete research?"
    )
    print(f"  is_complete: {result.is_complete}")
    print(f"  feedback: {result.overall_feedback[:100]}...")
    print("  [PASS]")
except Exception as e:
    print(f"  [FAIL] {e}")

# ─────────────────────────────────────────────────
# TEST 10: LLM Structured Output (FinalReport)
# ─────────────────────────────────────────────────
print("\n[TEST 10] LLM Structured Output - FinalReport")
try:
    from core.llm import get_llm
    from core.schemas import FinalReport
    llm = get_llm()
    structured = llm.with_structured_output(FinalReport)
    result = structured.invoke(
        "Write a short report about Python programming with 2 sections."
    )
    print(f"  Title: {result.title}")
    print(f"  Sections: {len(result.sections)}")
    for s in result.sections:
        print(f"    - {s.heading}: {s.content[:50]}...")
    print(f"  References: {len(result.references)}")
    print("  [PASS]")
except Exception as e:
    print(f"  [FAIL] {e}")

# ─────────────────────────────────────────────────
# TEST 11: Markdown Generation (with ReportSection)
# ─────────────────────────────────────────────────
print("\n[TEST 11] Markdown Generation")
try:
    from core.schemas import FinalReport, ReportSection
    from tools.markdown import generate_markdown
    report = FinalReport(
        title="Test Report",
        executive_summary="This is a test.",
        sections=[
            ReportSection(heading="Section 1", content="Content 1"),
            ReportSection(heading="Section 2", content="Content 2"),
        ],
        references=["https://example.com"],
    )
    path = generate_markdown(report)
    print(f"  Output: {path}")
    content = path.read_text(encoding='utf-8')
    print(f"  Content length: {len(content)}")
    print("  [PASS]")
except Exception as e:
    print(f"  [FAIL] {e}")

# ─────────────────────────────────────────────────
# TEST 12: PDF Generation
# ─────────────────────────────────────────────────
print("\n[TEST 12] PDF Generation")
try:
    from core.schemas import FinalReport, ReportSection
    from tools.markdown import generate_markdown
    from tools.pdf import markdown_to_pdf
    report = FinalReport(
        title="Test Report",
        executive_summary="This is a test.",
        sections=[
            ReportSection(heading="Sec1", content="Content1"),
        ],
        references=["https://example.com"],
    )
    md_path = generate_markdown(report)
    pdf_path = markdown_to_pdf(md_path)
    print(f"  PDF: {pdf_path}")
    assert pdf_path.exists(), "PDF not created"
    print("  [PASS]")
except Exception as e:
    print(f"  [FAIL] {e}")

print("\n" + "=" * 80)
print("DIAGNOSTIC COMPLETE")
print("=" * 80)
