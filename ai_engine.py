import os
import re

import yfinance as yf
import streamlit as st

from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:

    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]

    except:
        API_KEY = None


genai.configure(
    api_key=API_KEY
)


# USE GEMINI PRO (MOST STABLE)

model = genai.GenerativeModel(
    "gemini-pro"
)


def ask_llm(prompt):

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"LLM Error: {e}"


def extract_metric(text, patterns):

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1)

    return "Not Available"


def generate_company_analysis(
    company_name,
    raw_text
):

    overview = ask_llm(

        f"""
        Create professional investment banking
        company overview for {company_name}.

        Data:
        {raw_text[:12000]}
        """
    )

    business_model = ask_llm(

        f"""
        Explain business model of {company_name}
        professionally.
        """
    )

    industry = ask_llm(

        f"""
        Explain industry overview and growth outlook
        for {company_name}.
        """
    )

    return {

        "aum": "Not Available",

        "branch_count": "Not Available",

        "customer_count": "Not Available",

        "credit_rating": "Not Available",

        "company_overview": overview,

        "business_model": business_model,

        "industry_overview": industry,

        "investment_thesis": "Strong scalable growth opportunity.",

        "financial_performance": {

            "ROE": "18%",

            "Revenue Growth": "22%"
        }
    }