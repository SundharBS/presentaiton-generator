import re
import yfinance as yf
import google.generativeai as genai
import streamlit as st


# GEMINI CONFIG

genai.configure(

    api_key=st.secrets["GEMINI_API_KEY"]
)


model = genai.GenerativeModel(

    "gemini-1.5-flash"
)


# GEMINI FUNCTION

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

    return None


# YAHOO FINANCE

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


# MAIN FUNCTION

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


    # SECTOR

    sector_prompt = f"""

    Identify:

    1. Sector
    2. Industry

    for this company:

    {company_name}

    Information:

    {combined_text}

    Return format:

    Sector: ___
    Industry: ___
    """


    sector_info = ask_llm(

        sector_prompt
    )


    # COMPANY OVERVIEW

    overview_prompt = f"""

    Create a professional
    investment banking style
    company overview for:

    {company_name}

    Information:

    {combined_text}

    Use institutional language.
    """


    company_overview = ask_llm(

        overview_prompt
    )


    # BUSINESS MODEL

    business_prompt = f"""

    Explain the business model of:

    {company_name}

    Use investment banking
    and consulting style language.
    """


    business_model = ask_llm(

        business_prompt
    )


    # INDUSTRY OVERVIEW

    industry_prompt = f"""

    Create an industry overview for:

    {company_name}

    Mention:
    - growth
    - trends
    - opportunities
    - outlook
    """


    industry_overview = ask_llm(

        industry_prompt
    )


    # INVESTMENT THESIS

    thesis_prompt = f"""

    Create a professional
    investment thesis for:

    {company_name}

    Mention:
    - strengths
    - scalability
    - positioning
    - growth opportunities
    """


    investment_thesis = ask_llm(

        thesis_prompt
    )


    # EXTRACTED METRICS

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

        "sector":

        sector_info,


        "aum":

        str(

            market_data.get(

                "marketCap",

                "Not Available"
            )
        ),


        "branch_count":

        branch_count or "Not Available",


        "customer_count":

        customer_count or "Not Available",


        "employee_count":

        str(

            market_data.get(

                "fullTimeEmployees",

                "Not Available"
            )
        ),


        "credit_rating":

        credit_rating or "Not Available",


        "company_overview":

        company_overview,


        "business_model":

        business_model,


        "industry_overview":

        industry_overview,


        "financial_performance": {

            "Revenue Growth":

            str(

                market_data.get(

                    "revenueGrowth",

                    "Not Available"
                )
            ),


            "EBITDA Margin":

            str(

                market_data.get(

                    "ebitdaMargins",

                    "Not Available"
                )
            ),


            "ROE":

            str(

                market_data.get(

                    "returnOnEquity",

                    "Not Available"
                )
            ),


            "P/E":

            str(

                market_data.get(

                    "trailingPE",

                    "Not Available"
                )
            ),


            "Debt/Equity":

            str(

                market_data.get(

                    "debtToEquity",

                    "Not Available"
                )
            )
        },


        "risks": [

            "Macroeconomic slowdown",

            "Competitive intensity",

            "Regulatory changes"
        ],


        "investment_thesis":

        investment_thesis
    }