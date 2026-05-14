from pptx import Presentation


def add_slide(prs, title_text, body_text):

    slide_layout = prs.slide_layouts[1]

    slide = prs.slides.add_slide(
        slide_layout
    )

    title = slide.shapes.title

    body = slide.placeholders[1]

    title.text = title_text

    body.text = str(body_text)


def generate_ppt(
    company_name,
    analysis,
    selected_sections
):

    prs = Presentation()

    # TITLE SLIDE
    slide_layout = prs.slide_layouts[0]

    slide = prs.slides.add_slide(
        slide_layout
    )

    title = slide.shapes.title

    subtitle = slide.placeholders[1]

    title.text = f"{company_name} Investment Deck"

    subtitle.text = "Generated using AI"

    slides = [

        (
            "Client Situational Analysis",
            analysis.get(
                "client_situational_analysis",
                "Not Available"
            )
        ),

        (
            "Market & Industry Overview",
            analysis.get(
                "market_industry_overview",
                "Not Available"
            )
        ),

        (
            "Strategic Options / Thesis",
            analysis.get(
                "strategic_options_thesis",
                "Not Available"
            )
        ),

        (
            "Valuation Analysis",
            analysis.get(
                "valuation_analysis",
                "Not Available"
            )
        ),

        (
            "Key Considerations & Risk Factors",
            analysis.get(
                "key_considerations_risk_factors",
                "Not Available"
            )
        ),

        (
            "Appendices",
            analysis.get(
                "appendices",
                "Not Available"
            )
        )
    ]

    for heading, content in slides:

        if heading not in selected_sections:
            continue

        add_slide(
            prs,
            heading,
            content
        )

    ppt_path = f"{company_name}_Investment_Deck.pptx"

    prs.save(ppt_path)

    return ppt_path