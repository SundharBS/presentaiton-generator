import json

from ai_engine import generate_company_analysis
from ppt_generator import generate_ppt


def generate_pitch_deck(company_name, raw_text):

    prompt = f"""
    Analyze the following company information and provide output ONLY in valid JSON format.

    Required JSON structure:

    {{
        "overview": "",
        "business_model": "",
        "industry_overview": "",
        "aum": "",
        "branches": "",
        "customers": "",
        "credit_rating": ""
    }}

    Company Information:
    {raw_text}
    """

    analysis_text = generate_company_analysis(
        company_name,
        prompt
    )

    try:

        cleaned = (
            analysis_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        analysis = json.loads(cleaned)

    except Exception:

        analysis = {
            "overview": analysis_text,
            "business_model": analysis_text,
            "industry_overview": analysis_text,
            "aum": "Not Available",
            "branches": "Not Available",
            "customers": "Not Available",
            "credit_rating": "Not Available"
        }

    ppt_path = generate_ppt(
        company_name,
        analysis
    )

    return {
        "analysis": analysis,
        "ppt_path": ppt_path
    }