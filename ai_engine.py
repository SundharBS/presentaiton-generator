import os
import google.generativeai as genai
from dotenv import load_dotenv

# LOAD ENV VARIABLES
load_dotenv()

# CONFIGURE GEMINI API
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found")

genai.configure(api_key=api_key)

# LOAD MODEL
model = genai.GenerativeModel(
    "gemini-2.0-flash"
)

# GENERATE COMPANY ANALYSIS
def generate_company_analysis(company_name, prompt):

    try:

        full_prompt = f"""
        You are a professional investment banking analyst.

        Company Name:
        {company_name}

        Task:
        {prompt}

        Generate:
        - Company overview
        - Business model
        - Industry overview
        - Key strengths
        - Risks
        - Financial insights if available

        Keep output professional and concise.
        """

        response = model.generate_content(
            full_prompt
        )

        return response.text

    except Exception as e:

        return f"LLM Error: {str(e)}"