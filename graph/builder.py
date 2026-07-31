from langgraph.graph import StateGraph, START, END
from core.state import ResearchState
from graph.nodes import (
    plan_node,
    search_node,
    summarize_node,
    critic_node,
    write_node,
    save_report_node
)
from graph.edges import should_continue_research

def build_graph():
    builder = StateGraph(ResearchState)
    
    # Add nodes
    builder.add_node("plan", plan_node)
    builder.add_node("search", search_node)
    builder.add_node("summarize", summarize_node)
    builder.add_node("critic", critic_node)
    builder.add_node("write", write_node)
    builder.add_node("save_report", save_report_node)
    
    # Add edges
    builder.add_edge(START, "plan")
    builder.add_edge("plan", "search")
    builder.add_edge("search", "summarize")
    builder.add_edge("summarize", "critic")
    
    # Add conditional edges
    builder.add_conditional_edges(
        "critic",
        should_continue_research,
        {
            "search": "search",
            "write": "write"
        }
    )
    
    builder.add_edge("write", "save_report")
    builder.add_edge("save_report", END)
    
    return builder.compile()
