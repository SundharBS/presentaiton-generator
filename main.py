import json
import re

from ai_engine import generate_company_analysis
from ppt_generator import generate_ppt


def local_analysis(raw_text):

    def extract_section(keywords):

        lines = raw_text.split("\n")

        extracted = []

        for line in lines:

            for keyword in keywords:

                if keyword.lower() in line.lower():

                    extracted.append(line)

        return "\n".join(extracted[:20])

    overview = extract_section(
        [
            "overview",
            "company",
            "business",
            "about"
        ]
    )

    business_model = extract_section(
        [
            "products",
            "services",
            "revenue",
            "customers"
        ]
    )

    industry_overview = extract_section(
        [
            "industry",
            "market",
            "competition",
            "growth"
        ]
    )

    revenue_match = re.search(
        r"Revenue.*?(\d[\d,\.]+)",
        raw_text,
        re.IGNORECASE
    )

    aum = (
        revenue_match.group(1)
        if revenue_match
        else "Not Available"
    )

    return {
        "overview": overview or "Overview not found",
        "business_model": business_model or "Business model not found",
        "industry_overview": industry_overview or "Industry overview not found",
        "aum": aum,
        "branches": "Not Available",
        "customers": "Not Available",
        "credit_rating": "Not Available"
    }


def generate_pitch_deck(
    company_name,
    raw_text,
    use_ai=True
):

    # AI MODE
    if use_ai:

        prompt = f"""
        Analyze the following company information.

        Return ONLY valid JSON.

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

            analysis = local_analysis(raw_text)

    # LOCAL MODE
    else:

        analysis = local_analysis(raw_text)

    ppt_path = generate_ppt(
        company_name,
        analysis
    )

    return {
        "analysis": analysis,
        "ppt_path": ppt_path
    }