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
    "gemini-1.5-flash"
)

# GENERATE COMPANY ANALYSIS
def generate_company_analysis(company_name, prompt):

    try:
        full_prompt = f"""
        Company Name: {company_name}

        {prompt}

        Give detailed and professional investment style output.
        """

        response = model.generate_content(full_prompt)

        return response.text

    except Exception as e:
        return f"LLM Error: {str(e)}"