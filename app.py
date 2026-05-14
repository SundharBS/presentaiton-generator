import streamlit as st
from main import generate_pitch_deck
from auto_fetch import fetch_company_data

# PAGE CONFIG
st.set_page_config(
    page_title="AI Investment Deck Generator",
    layout="wide"
)

# TITLE
st.title("AI Investment Deck Generator")

st.markdown(
    "Generate professional investment pitch decks using AI"
)

# INPUTS
company_name = st.text_input(
    "Enter Company Name"
)

selected_sections = st.multiselect(
    "Select Sections",
    [
        "Overview",
        "Financials",
        "Operations",
        "Risks",
        "Valuation"
    ],
    default=[
        "Overview",
        "Financials",
        "Operations"
    ]
)

# GENERATE BUTTON
if st.button("Generate Investment Deck"):

    if not company_name:

        st.error(
            "Please enter company name"
        )

    else:

        with st.spinner(
            "Searching company documents..."
        ):

            raw_text = fetch_company_data(
                company_name
            )

        st.success(
            "Investment deck generated successfully"
        )

        # GENERATE PITCH DECK
        with st.spinner(
            "Generating investment deck..."
        ):

            result = generate_pitch_deck(
                company_name,
                raw_text
            )

        analysis = result["analysis"]

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
                    "branches",
                    "Not Available"
                )
            )

        with col3:

            st.metric(
                "Customers",
                analysis.get(
                    "customers",
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
        tab1, tab2, tab3 = st.tabs(
            [
                "Overview",
                "Business Model",
                "Industry Overview"
            ]
        )

        with tab1:

            st.header(
                "Company Overview"
            )

            st.write(
                analysis.get(
                    "overview",
                    "No overview available"
                )
            )

        with tab2:

            st.header(
                "Business Model"
            )

            st.write(
                analysis.get(
                    "business_model",
                    "No business model available"
                )
            )

        with tab3:

            st.header(
                "Industry Overview"
            )

            st.write(
                analysis.get(
                    "industry_overview",
                    "No industry overview available"
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