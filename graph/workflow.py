from graph.builder import build_graph
from core.state import ResearchState
from core.schemas import FinalReport

graph = build_graph()

def run_research(query: str) -> FinalReport:
    initial_state = {
        "user_query": query,
        "plan": [],
        "search_results": [],
        "summaries": [],
        "critic_review": None,
        "final_report": None,
        "iteration": 0
    }
    
    result = graph.invoke(initial_state)
    
    return result.get("final_report")
