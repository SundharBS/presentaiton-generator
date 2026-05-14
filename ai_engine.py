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


def generate_company_analysis(company_name, prompt):

    try:

        full_prompt = f"""
        You are a professional investment banking analyst.

        Company Name:
        {company_name}

        Task:
        {prompt}

        Generate:
        - Client Situational Analysis
        - Market & Industry Overview
        - Strategic Options / Thesis
        - Valuation Analysis
        - Key Considerations & Risk Factors
        - Appendices

        Keep output professional and concise.
        """

        response = model.generate_content(
            full_prompt
        )

        return response.text

    except Exception as e:

        return f"""
        {{
            "client_situational_analysis": "LLM Error",
            "market_industry_overview": "{str(e)}",
            "strategic_options_thesis": "Not Available",
            "valuation_analysis": "Not Available",
            "key_considerations_risk_factors": "Not Available",
            "appendices": "Not Available"
        }}
        """