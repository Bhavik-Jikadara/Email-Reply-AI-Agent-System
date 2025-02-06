from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.schema import Document
from src.chains import (
    email_category_chain,
    search_keyword_chain,
    draft_writer_chain
)
from utils.file_utils import write_markdown_file
from src.state import GraphState
from langchain_core.messages import AIMessage

def extract_text(result):
    """Helper function to extract text from various response types"""
    if isinstance(result, AIMessage):
        return result.content
    elif isinstance(result, dict):
        return str(result)
    return str(result)

def categorize_email(state: GraphState) -> dict:
    """Categorizes the incoming email."""
    print("🔍 Categorizing Email...")
    try:
        category_result = email_category_chain.invoke({"initial_email": state['initial_email']})
        email_category = extract_text(category_result).strip()
        
        # Validate category
        valid_categories = {
            'price_inquiry', 'customer_complaint', 'product_inquiry',
            'customer_feedback', 'off_topic'
        }
        
        if email_category not in valid_categories:
            email_category = 'product_inquiry'  # Default fallback
            
        write_markdown_file(email_category, "email_category", state['initial_email'])
        return {
            "email_category": email_category, 
            "num_steps": state['num_steps'] + 1
        }
    except Exception as e:
        print(f"Error in email categorization: {e}")
        return {
            "email_category": "product_inquiry",  # Default fallback category
            "num_steps": state['num_steps'] + 1
        }

def research_info_search(state: GraphState) -> dict:
    """Performs web research based on email content."""
    print("🔎 Researching Additional Information...")
    try:
        keywords_result = search_keyword_chain.invoke({
            "initial_email": state["initial_email"],
            "email_category": state["email_category"]
        })
        
        # Extract keywords safely
        keywords = []
        if isinstance(keywords_result, dict) and 'keywords' in keywords_result:
            keywords = keywords_result['keywords']
        if not keywords or not isinstance(keywords, list):
            keywords = ["default search term"]
        
        web_search_tool = TavilySearchResults(k=1)
        search_results = []
        
        for keyword in keywords[:1]:
            results = web_search_tool.invoke({"query": keyword})
            if results:
                content = "\n".join([d["content"] for d in results])
                search_results.append(Document(page_content=content))
        
        if not search_results:
            search_results.append(Document(page_content="No additional information found."))
            
        return {
            "research_info": search_results, 
            "num_steps": state['num_steps'] + 1
        }
    except Exception as e:
        print(f"Error in research search: {e}")
        return {
            "research_info": [Document(page_content="No additional information found.")],
            "num_steps": state['num_steps'] + 1
        }

def draft_email_writer(state: GraphState) -> dict:
    """Generates initial email draft."""
    print("✍️ Writing Draft Email...")
    try:
        draft_result = draft_writer_chain.invoke({
            "initial_email": state["initial_email"],
            "email_category": state["email_category"],
            "research_info": state["research_info"]
        })
        
        # Extract email draft safely
        email_draft = ""
        if isinstance(draft_result, dict):
            email_draft = draft_result.get('email_draft', '')
        else:
            email_draft = extract_text(draft_result)
            
        if not email_draft.strip():
            email_draft = "Thank you for your email. We will get back to you shortly."
            
        write_markdown_file(email_draft, "draft_email", state['initial_email'])
        return {
            "draft_email": email_draft, 
            "num_steps": state['num_steps'] + 1
        }
    
    except Exception as e:
        print(f"Error in generating draft email: {e}")
        default_response = "Thank you for your email. We will get back to you shortly."
        write_markdown_file(default_response, "draft_email", state['initial_email'])
        return {
            "draft_email": default_response,
            "num_steps": state['num_steps'] + 1
        }