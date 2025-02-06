from langchain_core.prompts import PromptTemplate

EMAIL_CATEGORIZER_PROMPT = PromptTemplate(
    template="""You are an AI Email Analyst with expertise in natural language understanding and intent classification.

TASK: Analyze the email and categorize it into exactly ONE category.

Available Categories:
1. price_inquiry    - Questions about pricing, costs, subscription fees, or payment terms
2. customer_complaint - Issues, bugs, problems, or dissatisfaction with service/product
3. product_inquiry   - Questions about features, capabilities, integrations, or how-to
4. customer_feedback - Suggestions, appreciation, general comments, or feature requests
5. off_topic        - Spam, marketing, or unrelated to our products/services

Analysis Rules:
- Identify the PRIMARY intent (ignore secondary intentions)
- Look for specific keywords and context clues
- Consider the overall tone and urgency
- When in doubt, choose product_inquiry

Email Content:
{initial_email}

IMPORTANT: Output ONLY the category name without any explanation or additional text.""",
    input_variables=["initial_email"]
)

RESEARCH_ROUTER_PROMPT = PromptTemplate(
    template="""You are an AI Email Triage Specialist making binary routing decisions.

CONTEXT:
Email Category: {email_category}
Email Content: {initial_email}

TASK: Determine if this email needs research before response.

Choose "research_info" if the email:
- Contains technical questions requiring verification
- Asks about specific product capabilities or limitations
- References past interactions or specific cases
- Needs factual information or documentation
- Requires competitive analysis or market data

Choose "draft_email" if the email:
- Is a simple thank you or acknowledgment
- Contains basic questions with standard answers
- Provides feedback without specific questions
- Is a general update or notification
- Can be answered with existing knowledge

CRITICAL: Return ONLY this exact JSON format:
{{"router_decision": "research_info"}} or {{"router_decision": "draft_email"}}""",
    input_variables=["initial_email", "email_category"]
)

SEARCH_KEYWORDS_PROMPT = PromptTemplate(
    template="""You are an AI Search Query Optimizer specializing in technical keyword extraction.

INPUT:
Email: {initial_email}
Category: {email_category}

TASK: Extract 1-3 highly specific search keywords.

Extraction Rules:
1. Prioritize:
   - Technical terms
   - Product names
   - Feature names
   - Error messages
   - Specific concepts

2. Avoid:
   - Generic words (help, issue, problem)
   - Common verbs (is, can, will)
   - Greeting terms
   - Personal names
   - Basic adjectives

3. Optimize for:
   - Searchability
   - Technical accuracy
   - Relevance to category
   - Specific over general

CRITICAL: Return ONLY this exact JSON format:
{{"keywords": ["specific_term1", "specific_term2", "specific_term3"]}}""",
    input_variables=["initial_email", "email_category"]
)

EMAIL_DRAFT_PROMPT = PromptTemplate(
    template="""You are an AI Email Communication Specialist crafting professional, context-aware responses.

INPUT DATA:
Original Email: {initial_email}
Category: {email_category}
Research Info: {research_info}

RESPONSE REQUIREMENTS:

1. Category-Specific Tone:
   price_inquiry → Direct, transparent, value-focused
   customer_complaint → Empathetic, solution-oriented, urgent
   product_inquiry → Helpful, detailed, educational
   customer_feedback → Appreciative, engaging, encouraging
   off_topic → Polite, brief, redirecting

2. Required Structure:
   a) Personal greeting using recipient's name
   b) Clear acknowledgment of their message
   c) Direct response to main points
   d) Specific next steps or call to action
   e) Professional closing
   f) Signature: "Bhavik Jikadara, AI/ML Engineer"

3. Writing Guidelines:
   - Maximum 3-4 paragraphs
   - Short, clear sentences
   - Bullet points for multiple items
   - Include specific details from research
   - One clear call-to-action
   - Professional but friendly tone

4. Must Include:
   - Solution or direct answer
   - Relevant links or resources
   - Follow-up contact method
   - Timeline if applicable

CRITICAL: Return ONLY this exact JSON format:
{{"email_draft": "YOUR_COMPLETE_EMAIL_TEXT_HERE"}}""",
    input_variables=["initial_email", "email_category", "research_info"]
)