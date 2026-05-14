import json
import re

from ppt_generator import generate_ppt

# SAFE AI IMPORT
try:

    from ai_engine import generate_company_analysis

    AI_AVAILABLE = True

except Exception:

    AI_AVAILABLE = False


def clean_text(text, max_lines=6):

    if not text:
        return "Not Available"

    lines = []

    for line in text.split("\n"):

        line = line.strip()

        if (
            line
            and len(line) > 20
            and line not in lines
        ):

            lines.append(f"• {line}")

    return "\n".join(lines[:max_lines])


def extract_section(raw_text, keywords):

    extracted = []

    lines = raw_text.split("\n")

    for line in lines:

        for keyword in keywords:

            if keyword.lower() in line.lower():

                extracted.append(line)

    return clean_text(
        "\n".join(extracted)
    )


def local_analysis(raw_text):

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

        "client_situational_analysis":
        extract_section(
            raw_text,
            [
                "overview",
                "business",
                "company",
                "operations"
            ]
        ),

        "market_industry_overview":
        extract_section(
            raw_text,
            [
                "industry",
                "market",
                "competition",
                "growth"
            ]
        ),

        "strategic_options_thesis":
        extract_section(
            raw_text,
            [
                "strategy",
                "expansion",
                "future",
                "opportunity"
            ]
        ),

        "valuation_analysis":
        f"""
• Estimated Revenue / Financial Indicator:
{revenue}

• Financial performance extracted from uploaded report

• Further valuation benchmarking recommended
        """,

        "key_considerations_risk_factors":
        extract_section(
            raw_text,
            [
                "risk",
                "challenge",
                "regulation",
                "debt",
                "default",
                "compliance"
            ]
        ),

        # COVER PAGE METRICS
        "aum": revenue,

        "growth": "Strong Growth",

        "gnpa": "Moderate Risk",

        "capital": "Well Capitalized"
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

            Keep every section concise and presentation-friendly.

            Return:

            {{
                "client_situational_analysis": "",
                "market_industry_overview": "",
                "strategic_options_thesis": "",
                "valuation_analysis": "",
                "key_considerations_risk_factors": "",

                "aum": "",
                "growth": "",
                "gnpa": "",
                "capital": ""
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

            analysis = local_analysis(
                raw_text
            )

    else:

        analysis = local_analysis(
            raw_text
        )

    ppt_path = generate_ppt(
        company_name,
        analysis,
        selected_sections
    )

    return {
        "analysis": analysis,
        "ppt_path": ppt_path
    }