import json
import re

from ppt_generator import generate_ppt

# SAFE AI IMPORT
try:

    from ai_engine import generate_company_analysis

    AI_AVAILABLE = True

except Exception:

    AI_AVAILABLE = False


def local_analysis(raw_text):

    def extract_section(keywords):

        lines = raw_text.split("\n")

        extracted = []

        for line in lines:

            for keyword in keywords:

                if keyword.lower() in line.lower():

                    extracted.append(line)

        return "\n".join(extracted[:25])

    revenue_match = re.search(
        r"Revenue.*?(\d[\d,\.]+)",
        raw_text,
        re.IGNORECASE
    )

    revenue = (
        revenue_match.group(1)
        if revenue_match
        else "Not Available"
    )

    return {

        "client_situational_analysis": extract_section(
            [
                "overview",
                "business",
                "company",
                "operations"
            ]
        ),

        "market_industry_overview": extract_section(
            [
                "industry",
                "market",
                "competition",
                "growth"
            ]
        ),

        "strategic_options_thesis": extract_section(
            [
                "strategy",
                "expansion",
                "future",
                "opportunity"
            ]
        ),

        "valuation_analysis": f"""
Estimated Revenue / Financial Indicator:
{revenue}
        """,

        "key_considerations_risk_factors": extract_section(
            [
                "risk",
                "challenge",
                "regulation",
                "debt"
            ]
        ),

        "appendices": "Generated from uploaded report / fetched company information."
    }


def generate_pitch_deck(
    company_name,
    raw_text,
    use_ai=True,
    selected_sections=None
):

    analysis = None

    # AI MODE
    if use_ai and AI_AVAILABLE:

        try:

            prompt = f"""
            You are an investment banking analyst.

            Analyze the company and return ONLY valid JSON.

            {{
                "client_situational_analysis": "",
                "market_industry_overview": "",
                "strategic_options_thesis": "",
                "valuation_analysis": "",
                "key_considerations_risk_factors": "",
                "appendices": ""
            }}

            Company Information:
            {raw_text}
            """

            analysis_text = generate_company_analysis(
                company_name,
                prompt
            )

            cleaned = (
                analysis_text
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            analysis = json.loads(cleaned)

        except Exception:

            analysis = local_analysis(raw_text)

    # LOCAL FALLBACK
    else:

        analysis = local_analysis(raw_text)

    ppt_path = generate_ppt(
        company_name,
        analysis,
        selected_sections
    )

    return {
        "analysis": analysis,
        "ppt_path": ppt_path
    }