from core.state import ResearchState
from config.settings import MAX_RESEARCH_ITERATIONS
from core.logger import logger

def should_continue_research(state: ResearchState) -> str:
    review = state.get("critic_review")
    iteration = state.get("iteration", 0)
    
    if review and review.is_complete:
        logger.info("Critic review is complete. Moving to write.")
        return "write"
        
    if iteration >= MAX_RESEARCH_ITERATIONS:
        logger.warning(f"Reached max iterations ({MAX_RESEARCH_ITERATIONS}). Forcing write.")
        return "write"
        
    logger.info("Critic review incomplete and max iterations not reached. Moving to search.")
    return "search"
