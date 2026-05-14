import os
import google.generativeai as genai
from dotenv import load_dotenv

# LOAD ENV
load_dotenv()

# CONFIGURE API
genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# LOAD MODEL
model = genai.GenerativeModel(
    "gemini-2.0-flash"
)


def generate_company_analysis(company_name, prompt):

    try:

        final_prompt = f"""
        You are a professional investment banking analyst.

        Company Name:
        {company_name}

        Task:
        {prompt}

        Generate concise and professional output.
        """

        response = model.generate_content(
            final_prompt
        )

        return response.text

    except Exception as e:

        return f"""
        {{
            "overview": "LLM Error",
            "business_model": "{str(e)}",
            "industry_overview": "Not Available",
            "aum": "Not Available",
            "branches": "Not Available",
            "customers": "Not Available",
            "credit_rating": "Not Available"
        }}
        """