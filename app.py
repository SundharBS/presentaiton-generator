import streamlit as st
import pdfplumber
from main import generate_pitch_deck

# PAGE CONFIG
st.set_page_config(
    page_title="AI Investment Deck Generator",
    layout="wide"
)

st.title("AI Investment Deck Generator")

st.markdown(
    "Upload annual reports or company PDFs to generate investment decks"
)

# COMPANY NAME
company_name = st.text_input(
    "Enter Company Name"
)

# PDF UPLOAD
uploaded_file = st.file_uploader(
    "Upload Annual Report / Investor Presentation",
    type=["pdf"]
)

# GENERATE BUTTON
if st.button("Generate Investment Deck"):

    if not company_name:

        st.error("Please enter company name")

    elif not uploaded_file:

        st.error("Please upload a PDF")

    else:

        with st.spinner("Extracting PDF text..."):

            raw_text = ""

            with pdfplumber.open(uploaded_file) as pdf:

                for page in pdf.pages:

                    text = page.extract_text()

                    if text:
                        raw_text += text + "\n"

        st.success("PDF processed successfully")

        with st.spinner("Generating investment deck..."):

            result = generate_pitch_deck(
                company_name,
                raw_text
            )

        analysis = result["analysis"]

        # METRICS
        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "AUM / Revenue",
                analysis.get("aum", "Not Available")
            )

        with col2:

            st.metric(
                "Branches",
                analysis.get("branches", "Not Available")
            )

        with col3:

            st.metric(
                "Customers",
                analysis.get("customers", "Not Available")
            )

        with col4:

            st.metric(
                "Credit Rating",
                analysis.get("credit_rating", "Not Available")
            )

        # OVERVIEW
        st.header("Company Overview")

        st.write(
            analysis.get(
                "overview",
                "No overview available"
            )
        )

        # BUSINESS MODEL
        st.header("Business Model")

        st.write(
            analysis.get(
                "business_model",
                "No business model available"
            )
        )

        # INDUSTRY OVERVIEW
        st.header("Industry Overview")

        st.write(
            analysis.get(
                "industry_overview",
                "No industry overview available"
            )
        )

        # DOWNLOAD PPT
        with open(result["ppt_path"], "rb") as file:

            st.download_button(
                label="Download Investment Deck",
                data=file,
                file_name=f"{company_name}_Investment_Deck.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )