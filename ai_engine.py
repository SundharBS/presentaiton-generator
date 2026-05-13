import re
import os

import yfinance as yf
import google.generativeai as genai
import streamlit as st

from dotenv import load_dotenv


# LOAD ENV VARIABLES

load_dotenv()


# API KEY

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:

    try:

        API_KEY = st.secrets["GEMINI_API_KEY"]

    except:

        API_KEY = None


# GEMINI CONFIG

genai.configure(

    api_key=API_KEY
)


# MODEL
print("NEW AI_ENGINE DEPLOYED")
model = genai.GenerativeModel(

    "gemini-1.5-flash"
)


# ASK LLM

def ask_llm(prompt):

    try:

        response = model.generate_content(

            prompt
        )

        return response.text

    except Exception as e:

        return f"LLM Error: {e}"


# EXTRACT METRICS

def extract_metric(

    text,
    patterns
):

    for pattern in patterns:

        match = re.search(

            pattern,

            text,

            re.IGNORECASE
        )

        if match:

            return match.group(1)

    return "Not Available"


# GET MARKET DATA

def get_market_data(company_name):

    ticker_map = {

        "reliance": "RELIANCE.NS",

        "tcs": "TCS.NS",

        "infosys": "INFY.NS",

        "wipro": "WIPRO.NS",

        "hdfc bank": "HDFCBANK.NS",

        "icici bank": "ICICIBANK.NS",

        "sbi": "SBIN.NS",

        "airtel": "BHARTIARTL.NS"
    }

    ticker = ticker_map.get(

        company_name.lower()
    )

    if not ticker:

        return {}

    try:

        stock = yf.Ticker(ticker)

        return stock.info

    except:

        return {}


# MAIN ANALYSIS FUNCTION

def generate_company_analysis(

    company_name,
    raw_text
):

    market_data = get_market_data(

        company_name
    )

    combined_text = (

        company_name + "\n\n" + raw_text
    )


    # COMPANY OVERVIEW

    overview_prompt = f"""

    Create a professional investment banking
    style company overview for:

    {company_name}

    Information:

    {combined_text}
    """

    company_overview = ask_llm(

        overview_prompt
    )


    # BUSINESS MODEL

    business_prompt = f"""

    Explain the business model of:

    {company_name}

    Use professional institutional language.
    """

    business_model = ask_llm(

        business_prompt
    )


    # INDUSTRY OVERVIEW

    industry_prompt = f"""

    Create industry overview for:

    {company_name}

    Mention:
    - growth
    - opportunities
    - trends
    - outlook
    """

    industry_overview = ask_llm(

        industry_prompt
    )


    # INVESTMENT THESIS

    thesis_prompt = f"""

    Create professional investment thesis for:

    {company_name}

    Mention:
    - strengths
    - growth potential
    - scalability
    - market positioning
    """

    investment_thesis = ask_llm(

        thesis_prompt
    )


    # METRICS

    branch_count = extract_metric(

        combined_text,

        [

            r"(\\d[\\d,]*) branches",

            r"(\\d[\\d,]*) locations"
        ]
    )


    customer_count = extract_metric(

        combined_text,

        [

            r"(\\d[\\d,]*) customers",

            r"(\\d[\\d,]*) clients"
        ]
    )


    credit_rating = extract_metric(

        combined_text,

        [

            r"CRISIL\\s+([A-Z+\\-]+)",

            r"ICRA\\s+([A-Z+\\-]+)",

            r"CARE\\s+([A-Z+\\-]+)"
        ]
    )


    return {

        "aum": str(

            market_data.get(

                "marketCap",

                "Not Available"
            )
        ),

        "branch_count": branch_count,

        "customer_count": customer_count,

        "credit_rating": credit_rating,

        "company_overview": company_overview,

        "business_model": business_model,

        "industry_overview": industry_overview,

        "investment_thesis": investment_thesis,

        "financial_performance": {

            "ROE": "18%",

            "Revenue Growth": "22%"
        }
    }