import streamlit as st
import os

from main import generate_pitch_deck
from pdf_reader import extract_pdf_text
from auto_fetch import (
    find_company_documents,
    download_company_documents
)


# PAGE CONFIG

st.set_page_config(

    page_title="AI Investment Deck Generator",

    layout="wide"
)


# CREATE REQUIRED FOLDERS

os.makedirs(

    "documents",

    exist_ok=True
)

os.makedirs(

    "output",

    exist_ok=True
)


# TITLE

st.title(

    "AI Investment Deck Generator"
)


st.markdown(

    """
    Generate professional investment banking style
    pitch decks automatically using AI.
    """
)


# INPUTS

company_name = st.text_input(

    "Enter Company Name"
)


uploaded_file = st.file_uploader(

    "Upload Annual Report (Optional)",

    type=["pdf"]
)


# SECTIONS

selected_sections = st.multiselect(

    "Select Sections",

    [

        "Overview",

        "Financials",

        "Operations",

        "Advisory"
    ],

    default=[

        "Overview",

        "Financials",

        "Operations"
    ]
)


# GENERATE BUTTON

if st.button(

    "Generate Investment Deck"
):

    if company_name or uploaded_file:

        raw_text = ""


        # USER UPLOADED PDF

        if uploaded_file:

            st.info(

                "Reading uploaded annual report..."
            )

            raw_text += extract_pdf_text(

                uploaded_file
            )


        # AUTO FETCH DOCUMENTS

        if len(raw_text) < 1000 and company_name:

            st.info(

                "Searching company documents..."
            )

            pdf_links = find_company_documents(

                company_name
            )

            downloaded_files = download_company_documents(

                company_name,

                pdf_links
            )


            for file_path in downloaded_files:

                try:

                    with open(

                        file_path,

                        "rb"
                    ) as file:

                        raw_text += extract_pdf_text(

                            file
                        )

                except:
                    pass


        # FALLBACK TEXT

        if len(raw_text.strip()) < 500:

            raw_text = f"""

            {company_name} is an Indian company
            with scalable operations,
            customer-focused growth strategy,
            and institutional expansion potential.

            The company focuses on operational efficiency,
            technology adoption,
            market expansion,
            and long-term growth opportunities.
            """


        # GENERATE ANALYSIS + PPT

        with st.spinner(

            "Generating investment deck..."
        ):

            result = generate_pitch_deck(

                company_name,

                raw_text,

                selected_sections
            )


        analysis = result["analysis"]

        ppt_path = result["ppt_path"]


        st.success(

            "Investment deck generated successfully"
        )


        # METRICS

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(

                "AUM / Market Cap",

                analysis.get(

                    "aum",

                    "Not Available"
                )
            )


        with col2:

            st.metric(

                "Branches",

                analysis.get(

                    "branch_count",

                    "Not Available"
                )
            )


        with col3:

            st.metric(

                "Customers",

                analysis.get(

                    "customer_count",

                    "Not Available"
                )
            )


        with col4:

            st.metric(

                "Credit Rating",

                analysis.get(

                    "credit_rating",

                    "Not Available"
                )
            )


        # TABS

        tab1, tab2, tab3 = st.tabs([

            "Overview",

            "Business Model",

            "Industry Overview"
        ])


        with tab1:

            st.subheader(

                "Company Overview"
            )

            st.write(

                analysis.get(

                    "company_overview",

                    ""
                )
            )


        with tab2:

            st.subheader(

                "Business Model"
            )

            st.write(

                analysis.get(

                    "business_model",

                    ""
                )
            )


        with tab3:

            st.subheader(

                "Industry Overview"
            )

            st.write(

                analysis.get(

                    "industry_overview",

                    ""
                )
            )


        # DOWNLOAD BUTTON

        if os.path.exists(

            ppt_path
        ):

            with open(

                ppt_path,

                "rb"
            ) as file:

                st.download_button(

                    label="Download Investment Deck",

                    data=file,

                    file_name=os.path.basename(

                        ppt_path
                    ),

                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )

    else:

        st.error(

            "Please enter company name or upload annual report."
        )