from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.messages import AIMessage
from src.config import GROQ_API_KEY, MODEL_NAME
from src.prompts import (
    EMAIL_CATEGORIZER_PROMPT,
    RESEARCH_ROUTER_PROMPT,
    SEARCH_KEYWORDS_PROMPT,
    EMAIL_DRAFT_PROMPT
)
import json

# Initialize LLM with temperature settings
GROQ_LLM = ChatGroq(
    api_key=GROQ_API_KEY, 
    model=MODEL_NAME,
    temperature=0.1  # Lower temperature for more consistent outputs
)

def create_json_parser_with_fallback():
    """Creates a JSON parser with error handling"""
    parser = JsonOutputParser()
    
    def parse_with_fallback(text_or_message) -> dict:
        try:
            # Handle AIMessage objects
            if isinstance(text_or_message, AIMessage):
                text = text_or_message.content
            else:
                text = str(text_or_message)

            # First try direct parsing
            try:
                return json.loads(text)
            except:
                pass

            # Clean and try parsing again
            clean_text = text.strip()
            start = clean_text.find('{')
            end = clean_text.rfind('}')
            
            if start != -1 and end != -1:
                try:
                    json_str = clean_text[start:end+1]
                    return json.loads(json_str)
                except:
                    pass

            # For research router specifically
            if "router_decision" in text.lower():
                if "research_info" in text.lower():
                    return {"router_decision": "research_info"}
                else:
                    return {"router_decision": "draft_email"}

            # If all parsing attempts fail, extract from text or return default
            if "email_draft" in text.lower():
                # For email drafts, preserve the full text
                return {"email_draft": text}
            elif "keywords" in text.lower():
                # For keywords, try to extract them
                return {"keywords": ["default_keyword"]}
            else:
                return {"error": "Parsing failed", "original_text": text}

        except Exception as e:
            return {"error": str(e), "original_text": str(text_or_message)}

    return parse_with_fallback

# Initialize Chains with improved error handling
email_category_chain = (
    EMAIL_CATEGORIZER_PROMPT 
    | GROQ_LLM 
    | (lambda x: x.content if isinstance(x, AIMessage) else str(x))
)

research_router_chain = (
    RESEARCH_ROUTER_PROMPT 
    | GROQ_LLM 
    | create_json_parser_with_fallback()
)

search_keyword_chain = (
    SEARCH_KEYWORDS_PROMPT 
    | GROQ_LLM 
    | create_json_parser_with_fallback()
)

draft_writer_chain = (
    EMAIL_DRAFT_PROMPT 
    | GROQ_LLM 
    | create_json_parser_with_fallback()
)