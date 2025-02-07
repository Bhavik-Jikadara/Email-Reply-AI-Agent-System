import streamlit as st
from src.workflow import create_workflow
import json

def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'current_email' not in st.session_state:
        st.session_state.current_email = None
    if 'current_response' not in st.session_state:
        st.session_state.current_response = None
    if 'response_counter' not in st.session_state:
        st.session_state.response_counter = 0

def display_header():
    st.title("✉️ Email Response Generator")

def display_input_section():
    with st.container():
        st.markdown('<p class="section-title">📝 Input Email</p>', unsafe_allow_html=True)
        email_content = st.text_area(
            label="",
            placeholder="""Hi, Bhavik!

It's Day 2 of your automation adventure with Apify, and it's time to connect the dots! 
Integrating your Actors with other solutions you use opens up a world of possibilities, 
making your workflows smarter and your life easier.

Have fun!

The Bhavik Team""",
            height=400,
            key="email_input"
        )
        
        generate_button = st.button(
            "🚀 Generate Response",
            key="generate_button",
            use_container_width=True,
            type="primary"
        )
        
        if st.session_state.history:
            with st.expander("📚 Previous Emails", expanded=False):
                for idx, item in enumerate(st.session_state.history):
                    st.text_area(
                        f"Email {idx + 1}",
                        item["email"],
                        height=400,
                        key=f"history_email_{idx}"
                    )
                    st.markdown("---")
        
        return email_content, generate_button
    
def extract_email_draft(response_text: str) -> str:
    """Extract email draft from the response text."""
    try:
        # Try parsing as JSON first
        if isinstance(response_text, str):
            try:
                json_response = json.loads(response_text)
                if isinstance(json_response, dict) and 'email_draft' in json_response:
                    return json_response['email_draft']
            except json.JSONDecodeError:
                pass

        # If JSON parsing fails, try extracting using string manipulation
        if '"email_draft":' in response_text:
            # Find the start of the email draft
            start_idx = response_text.find('"email_draft":') + len('"email_draft":')
            # Find the content between quotes
            content_start = response_text.find('"', start_idx) + 1
            content_end = response_text.rfind('"')
            if content_start < content_end:
                return response_text[content_start:content_end]

        # If all extraction methods fail, return the original text
        return response_text
    except Exception as e:
        print(f"Error extracting email draft: {e}")
        return response_text

def process_email(email_content):
    try:
        with st.spinner("🔄 Processing your email..."):
            app = create_workflow()
            inputs = {
                "initial_email": email_content,
                "research_info": None,
                "num_steps": 0
            }
            output = app.invoke(inputs)
            response = output.get('draft_email', 'Unable to process email')
            
            # Extract just the email draft text
            clean_response = extract_email_draft(response)
            return clean_response, None
    except Exception as e:
        return None, str(e)

def display_response_section(response, is_new=False):
    if is_new:
        st.session_state.response_counter += 1
    
    response_id = st.session_state.response_counter
    
    if response:
        st.markdown('<p class="section-title">📨 Generated Response</p>', unsafe_allow_html=True)
        tabs = st.tabs(["✏️ Editor", "👀 Preview", "💾 Drafts"])
        
        with tabs[0]:
            edited_response = st.text_area(
                label="",
                value=response,
                height=400,
                key=f"response_editor_{response_id}"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 Copy to Clipboard", 
                            key=f"copy_{response_id}",
                            use_container_width=True):
                    st.toast("Response copied to clipboard! 📋")
            with col2:
                if st.button("💾 Save Draft", 
                            key=f"save_{response_id}",
                            use_container_width=True):
                    st.session_state.history.append({
                        "email": st.session_state.current_email,
                        "response": edited_response
                    })
                    st.toast("Draft saved! 💾")
        
        with tabs[1]:
            st.markdown(f"""<div style="background-color: #2D2D2D; padding: 20px; border-radius: 8px; border: 1px solid #404040;">
                <pre style="color: #FFFFFF; margin: 0;">{response}</pre>
            </div>""", unsafe_allow_html=True)
        
        with tabs[2]:
            if st.session_state.history:
                for idx, item in enumerate(reversed(st.session_state.history)):
                    with st.expander(f"Draft {len(st.session_state.history) - idx}", expanded=False):
                        st.text_area(
                            "Response",
                            item["response"],
                            height=200,
                            key=f"draft_response_{response_id}_{idx}"
                        )
            else:
                st.info("No saved drafts yet!")

def main():
    st.set_page_config(
        page_title="AI ER Agent",
        page_icon="✉️",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={
            'Get help': None,  # Remove help link
            'Report a bug': None,  # Remove bug report link
            'About': None  # Remove about link
        }
    )
    
    initialize_session_state()
    display_header()
    
    # Create two columns with a bit more space for the response
    col1, col2 = st.columns([4, 5])
    
    with col1:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        email_content, generate_clicked = display_input_section()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        if generate_clicked and email_content:
            st.session_state.current_email = email_content
            response, error = process_email(email_content)
            
            if error:
                st.error(f"❌ An error occurred: {error}")
            else:
                st.session_state.current_response = response
                display_response_section(response, is_new=True)
        
        elif st.session_state.current_response:
            display_response_section(st.session_state.current_response)
        
        else:
            st.info("Generate a response to see it here!")
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
