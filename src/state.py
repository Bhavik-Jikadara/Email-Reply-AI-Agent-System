from typing import List, TypedDict

class GraphState(TypedDict):
    """State management for the email processing workflow."""
    initial_email: str
    email_category: str
    draft_email: str
    final_email: str
    research_info: List[str]
    info_needed: bool
    num_steps: int
    draft_email_feedback: dict