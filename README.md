# AI Email Reply Agent

A Streamlit application that automatically processes and generates responses to customer emails using AI. The app uses [LangChain](https://python.langchain.com/) and [Groq](https://groq.com/) for natural language processing and understanding.

## Key Features

- **Email Categorization**: Automatically categorizes emails into specific categories like price inquiries, customer complaints, product inquiries, customer feedback, and off-topic emails.
- **Automatic Research**: Performs web searches for complex queries or specific product details using the Tavily API.
- **Professional Response Generation**: Generates tailored, professional email responses using the Groq API.
- **Streamlit Interface**: A user-friendly web interface to input email content, view categorization, see research, and generate responses in real-time.

## Project Structure

- **`src/`**: Contains the main application code
  - `chains.py`: Logic for categorizing emails, conducting research, and generating responses.
  - `config.py`: Configuration and environment variable loading.
  - `processors.py`: Functions for processing emails, performing research, and drafting responses.
  - `prompts.py`: Templates used for AI prompt generation.
  - `state.py`: State management for the email processing workflow.
  - `workflow.py`: Defines the workflow using state graphs for processing emails.
- **`utils/`**: Utility functions for file operations and other helper tasks.
- **`outputs/`**: Stores generated response files like email drafts and research info.
- **`.env`**: Environment variables for API keys (Groq, Tavily).

## Setup

1. Clone the repository

   ```bash
   git clone https://github.com/Bhavik-Jikadara/AI-Email-Reply-Agent.git
   cd AI-Email-Reply-Agent
   ```

2. Create a virtualenv (windows user)

    ```bash
    pip install virtualenv
    virtualenv venv
    
    # windows users
    source venv/Scripts/activate
    
    # mac users
    source venv/bin/activate
    ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a .env file with your API keys:
   - [GROQ_API_KEY](https://console.groq.com/keys)
   - [TAVILY_API_KEY](https://app.tavily.com/)

   ```bash
   GROQ_API_KEY=your_groq_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

5. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

## Usage

1. Open the Streamlit app in your browser
2. Enter the email content in the text area
3. Click "Generate Response"
4. View the generated professional response

## License

[MIT](LICENSE)
