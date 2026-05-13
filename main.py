from ai_engine import generate_company_analysis

from ppt_generator import generate_ppt


def generate_pitch_deck(

    company_name,
    raw_text,
    selected_sections
):

    analysis = generate_company_analysis(

        company_name,
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