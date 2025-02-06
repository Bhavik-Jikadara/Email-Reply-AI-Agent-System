from langgraph.graph import END, StateGraph
from src.state import GraphState
from src.processors import categorize_email, research_info_search, draft_email_writer
from src.chains import research_router_chain

def create_workflow():
    """Creates and returns the workflow graph."""
    workflow = StateGraph(GraphState)
    
    # Add Nodes
    workflow.add_node("categorize_email", categorize_email)
    workflow.add_node("research_info_search", research_info_search)
    workflow.add_node("draft_email_writer", draft_email_writer)
    
    # Add Edges
    workflow.set_entry_point("categorize_email")
    workflow.add_conditional_edges(
        "categorize_email",
        lambda state: "research_info" if research_router_chain.invoke({
            "initial_email": state["initial_email"],
            "email_category": state["email_category"]
        })['router_decision'] == 'research_info' else "draft_email",
        {
            "research_info": "research_info_search",
            "draft_email": "draft_email_writer",
        }
    )
    workflow.add_edge("research_info_search", "draft_email_writer")
    workflow.add_edge("draft_email_writer", END)
    
    return workflow.compile()