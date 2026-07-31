from core.state import ResearchState
from core.logger import logger
from core.schemas import SearchPlan
from agents.planner import PlannerAgent
from agents.search import SearchAgent
from agents.summarizer import SummarizerAgent
from agents.critic import CriticAgent
from agents.writer import WriterAgent
from tools.markdown import generate_markdown
from tools.pdf import markdown_to_pdf

planner_agent = PlannerAgent()
search_agent = SearchAgent()
summarizer_agent = SummarizerAgent()
critic_agent = CriticAgent()
writer_agent = WriterAgent()


def plan_node(state: ResearchState) -> dict:
    logger.info("--- PLAN NODE ---")
    query = state.get("user_query")
    plan = planner_agent.plan(query)
    return {"plan": plan.tasks}


def search_node(state: ResearchState) -> dict:
    logger.info("--- SEARCH NODE ---")

    critic_review = state.get("critic_review")

    if critic_review and not critic_review.is_complete and critic_review.additional_search_queries:
        logger.info("Performing additional searches based on critic feedback.")
        new_results = search_agent.search_queries(critic_review.additional_search_queries)
    else:
        logger.info("Performing initial search based on plan.")
        plan = SearchPlan(tasks=state.get("plan", []))
        new_results = search_agent.search(plan)

    # Only store the NEW results for summarization.
    # Previous results are already captured in existing summaries.
    return {"search_results": new_results}


def summarize_node(state: ResearchState) -> dict:
    logger.info("--- SUMMARIZE NODE ---")

    # Summarize only the current batch of search_results
    new_summaries = summarizer_agent.summarize(state.get("search_results", []))

    # Merge with any existing summaries from previous iterations
    existing_summaries = state.get("summaries", []) or []

    all_summaries = existing_summaries + new_summaries

    logger.info(f"Summaries: {len(existing_summaries)} existing + {len(new_summaries)} new = {len(all_summaries)} total")

    return {"summaries": all_summaries}


def critic_node(state: ResearchState) -> dict:
    logger.info("--- CRITIC NODE ---")
    query = state.get("user_query")
    summaries = state.get("summaries", [])
    review = critic_agent.review(query, summaries)

    current_iteration = state.get("iteration", 0)

    logger.info(f"Critic: is_complete={review.is_complete}, iteration={current_iteration + 1}")

    return {
        "critic_review": review,
        "iteration": current_iteration + 1,
    }


def write_node(state: ResearchState) -> dict:
    logger.info("--- WRITE NODE ---")
    query = state.get("user_query")
    summaries = state.get("summaries", [])
    report = writer_agent.write(query, summaries)
    return {"final_report": report}


def save_report_node(state: ResearchState) -> dict:
    logger.info("--- SAVE REPORT NODE ---")
    report = state.get("final_report")
    if report:
        md_path = generate_markdown(report)
        pdf_path = markdown_to_pdf(md_path)
        logger.info(f"Report saved to markdown: {md_path}")
        logger.info(f"Report saved to pdf: {pdf_path}")
    return {}
