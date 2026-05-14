import streamlit as st
import pdfplumber

from auto_fetch import fetch_company_data
from main import generate_pitch_deck

# PAGE CONFIG
st.set_page_config(
    page_title="AI Investment Deck Generator",
    layout="wide"
)

# TITLE
st.title("AI Investment Deck Generator")

st.markdown(
    """
    Generate professional investment banking style PPTs

    • Upload annual reports for local generation  
    • Or use AI-powered company analysis
    """
)

# COMPANY NAME
company_name = st.text_input(
    "Enter Company Name"
)

# SECTION SELECTION
selected_sections = st.multiselect(
    "Select Sections to Include",
    [
        "Client Situational Analysis",
        "Market & Industry Overview",
        "Strategic Options / Thesis",
        "Valuation Analysis",
        "Key Considerations & Risk Factors",
        "Appendices"
    ],
    default=[
        "Client Situational Analysis",
        "Market & Industry Overview",
        "Strategic Options / Thesis",
        "Valuation Analysis"
    ]
)

# PDF UPLOAD
uploaded_file = st.file_uploader(
    "Upload Annual Report (Optional)",
    type=["pdf"]
)

# GENERATE BUTTON
if st.button("Generate Investment Deck"):

    if not company_name:

        st.error(
            "Please enter company name"
        )

    elif len(selected_sections) == 0:

        st.error(
            "Please select at least one section"
        )

    else:

        raw_text = ""

        # PDF MODE
        if uploaded_file:

            with st.spinner(
                "Extracting PDF text..."
            ):

                with pdfplumber.open(uploaded_file) as pdf:

                    for page in pdf.pages:

                        text = page.extract_text()

                        if text:
                            raw_text += text + "\n"

            use_ai = False

            st.success(
                "Using local report-based generation"
            )

        # AI MODE
        else:

            with st.spinner(
                "Fetching company data..."
            ):

                raw_text = fetch_company_data(
                    company_name
                )

            use_ai = True

            st.success(
                "Using AI-powered company analysis"
            )

        # GENERATE DECK
        with st.spinner(
            "Generating investment deck..."
        ):

            result = generate_pitch_deck(
                company_name,
                raw_text,
                use_ai,
                selected_sections
            )

        analysis = result["analysis"]

        # DISPLAY SECTIONS

        if "Client Situational Analysis" in selected_sections:

            st.header(
                "Client Situational Analysis"
            )

            st.write(
                analysis.get(
                    "client_situational_analysis",
                    "Not Available"
                )
            )

        if "Market & Industry Overview" in selected_sections:

            st.header(
                "Market & Industry Overview"
            )

            st.write(
                analysis.get(
                    "market_industry_overview",
                    "Not Available"
                )
            )

        if "Strategic Options / Thesis" in selected_sections:

            st.header(
                "Strategic Options / Thesis"
            )

            st.write(
                analysis.get(
                    "strategic_options_thesis",
                    "Not Available"
                )
            )

        if "Valuation Analysis" in selected_sections:

            st.header(
                "Valuation Analysis"
            )

            st.write(
                analysis.get(
                    "valuation_analysis",
                    "Not Available"
                )
            )

        if "Key Considerations & Risk Factors" in selected_sections:

            st.header(
                "Key Considerations & Risk Factors"
            )

            st.write(
                analysis.get(
                    "key_considerations_risk_factors",
                    "Not Available"
                )
            )

        if "Appendices" in selected_sections:

            st.header(
                "Appendices"
            )

            st.write(
                analysis.get(
                    "appendices",
                    "Not Available"
                )
            )

        # DOWNLOAD PPT
        with open(
            result["ppt_path"],
            "rb"
        ) as file:

            st.download_button(
                label="Download Investment Deck",
                data=file,
                file_name=f"{company_name}_Investment_Deck.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )