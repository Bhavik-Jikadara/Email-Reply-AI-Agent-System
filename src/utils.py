from typing import List
from typing_extensions import TypedDict
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()


# Llama3 model
GROQ_LLM = ChatGroq(model="llama3-70b-8192")


# Output save in .md file
def write_markdown_file(content, filename):
    """Writes the given content as a markdown file to the local directory.

    Args:
      content: The string content to write to the file.
      filename: The filename to save the file as.
    """
    with open(f"{filename}.md", "w") as f:
        f.write(content)


# Tool setup - Search
web_search_tool = TavilySearchResults(k=1)


# ===================== State ===================================
class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        initial_email: email
        email_category: email category
        draft_email: LLM generation
        final_email: LLM generation
        research_info: list of documents
        info_needed: whether to add search info
        num_steps: number of steps
    """
    initial_email: str
    email_category: str
    draft_email: str
    final_email: str
    research_info: List[str]
    info_needed: bool
    num_steps: int
    draft_email_feedback: dict


# State print

def state_printer(state):
    """print the state"""
    print("---STATE PRINTER---")
    print(f"Initial Email: {state['initial_email']} \n" )
    print(f"Email Category: {state['email_category']} \n")
    print(f"Draft Email: {state['draft_email']} \n" )
    print(f"Final Email: {state['final_email']} \n" )
    print(f"Research Info: {state['research_info']} \n")
    print(f"Info Needed: {state['info_needed']} \n")
    print(f"Num Steps: {state['num_steps']} \n")