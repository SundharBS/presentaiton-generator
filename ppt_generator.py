from pptx import Presentation


def generate_ppt(company_name, analysis):

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

    # CONTENT SLIDES
    sections = [
        ("Company Overview", analysis.get("overview", "")),
        ("Business Model", analysis.get("business_model", "")),
        ("Industry Overview", analysis.get("industry_overview", ""))
    ]

    for heading, content in sections:

        slide_layout = prs.slide_layouts[1]

        slide = prs.slides.add_slide(
            slide_layout
        )

        title = slide.shapes.title

        body = slide.placeholders[1]

        title.text = heading

        body.text = content

    ppt_path = f"{company_name}_Investment_Deck.pptx"

    prs.save(ppt_path)

    return ppt_path