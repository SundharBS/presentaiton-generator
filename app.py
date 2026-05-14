import streamlit as st
import pdfplumber

from auto_fetch import fetch_company_data
from main import generate_pitch_deck

# PAGE CONFIG
st.set_page_config(
    page_title="AI Investment Deck Generator",
    layout="wide"
)

st.title("AI Investment Deck Generator")

st.markdown(
    """
    • Upload annual reports for local PPT generation  
    • Or enter company name for AI-powered analysis
    """
)

# COMPANY NAME
company_name = st.text_input(
    "Enter Company Name"
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
                "Using local template generation"
            )

        # AI FETCH MODE
        else:

            with st.spinner(
                "Fetching company data..."
            ):

                raw_text = fetch_company_data(
                    company_name
                )

            use_ai = True

            st.success(
                "Using AI-powered generation"
            )

        # GENERATE DECK
        with st.spinner(
            "Generating investment deck..."
        ):

            result = generate_pitch_deck(
                company_name,
                raw_text,
                use_ai
            )

        analysis = result["analysis"]

        # DISPLAY
        st.header("Company Overview")

        st.write(
            analysis.get(
                "overview",
                "Not Available"
            )
        )

        st.header("Business Model")

        st.write(
            analysis.get(
                "business_model",
                "Not Available"
            )
        )

        st.header("Industry Overview")

        st.write(
            analysis.get(
                "industry_overview",
                "Not Available"
            )
        )

        # DOWNLOAD
        with open(
            result["ppt_path"],
            "rb"
        ) as file:

            st.download_button(
                label="Download PPT",
                data=file,
                file_name=f"{company_name}_Investment_Deck.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )