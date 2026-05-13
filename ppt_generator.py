import os

from pptx import Presentation


# REPLACE TEXT

def replace_text(

    shape,
    replacements
):

    if not shape.has_text_frame:

        return


    for paragraph in shape.text_frame.paragraphs:

        for run in paragraph.runs:

            text = run.text


            for key, value in replacements.items():

                text = text.replace(

                    key,

                    str(value)
                )


            run.text = text


# MAIN PPT FUNCTION

def generate_ppt(

    company_name,
    analysis,
    selected_sections
):

    prs = Presentation(

        "template.pptx"
    )


    replacements = {

        "UGRO Capital":

        company_name,


        "₹12,003 Cr":

        analysis["aum"],


        "2.3%":

        analysis["financial_performance"].get(

            "ROE",

            "N/A"
        ),


        "33%":

        analysis["financial_performance"].get(

            "Revenue Growth",

            "N/A"
        ),


        "India's Premier DataTech MSME Lender":

        analysis["company_overview"],


        "MSME Accha Hai! — Expanding Horizons":

        analysis["investment_thesis"]
    }


    for slide in prs.slides:

        for shape in slide.shapes:

            replace_text(

                shape,
                replacements
            )


    os.makedirs(

        "output",

        exist_ok=True
    )


    output_path = os.path.join(

        "output",

        f"{company_name}_Investment_Deck.pptx"
    )


    prs.save(

        output_path
    )


    return output_path