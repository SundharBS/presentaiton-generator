from pptx import Presentation
from pptx.util import Inches


def generate_ppt(company_name, analysis):

    prs = Presentation()

    # TITLE SLIDE
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)

    title = slide.shapes.title
    subtitle = slide.placeholders[1]

    title.text = f"{company_name} Investment Deck"
    subtitle.text = "Generated using AI"

    # OVERVIEW SLIDE
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)

    title = slide.shapes.title
    body = slide.placeholders[1]

    title.text = "Company Overview"

    body.text = analysis.get(
        "overview",
        "No overview available"
    )

    # BUSINESS MODEL SLIDE
    slide = prs.slides.add_slide(slide_layout)

    title = slide.shapes.title
    body = slide.placeholders[1]

    title.text = "Business Model"

    body.text = analysis.get(
        "business_model",
        "No business model available"
    )

    # INDUSTRY OVERVIEW SLIDE
    slide = prs.slides.add_slide(slide_layout)

    title = slide.shapes.title
    body = slide.placeholders[1]

    title.text = "Industry Overview"

    body.text = analysis.get(
        "industry_overview",
        "No industry overview available"
    )

    # SAVE PPT
    ppt_path = f"{company_name}_Investment_Deck.pptx"

    prs.save(ppt_path)

    return ppt_path