from src.utils import GraphState, state_printer
from src.nodes import categorize_email, research_info_search, draft_email_writer, analyze_draft_email, rewrite_email, no_rewrite
from src.edges import route_to_research, route_to_rewrite
from langgraph.graph import END, StateGraph

# Add nodes
workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("categorize_email", categorize_email)  # categorize email
workflow.add_node("research_info_search", research_info_search)  # web search
workflow.add_node("state_printer", state_printer)
workflow.add_node("draft_email_writer", draft_email_writer)
workflow.add_node("analyze_draft_email", analyze_draft_email)
workflow.add_node("rewrite_email", rewrite_email)
workflow.add_node("no_rewrite", no_rewrite)


# Add edges

workflow.set_entry_point("categorize_email")

workflow.add_conditional_edges(
    "categorize_email",
    route_to_research,
    {
        "research_info": "research_info_search",
        "draft_email": "draft_email_writer",
    },
)
workflow.add_edge("research_info_search", "draft_email_writer")


workflow.add_conditional_edges(
    "draft_email_writer",
    route_to_rewrite,
    {
        "rewrite": "analyze_draft_email",
        "no_rewrite": "no_rewrite",
    },
)
workflow.add_edge("analyze_draft_email", "rewrite_email")
workflow.add_edge("no_rewrite", "state_printer")
workflow.add_edge("rewrite_email", "state_printer")
workflow.add_edge("state_printer", END)

# Compile
app = workflow.compile()
