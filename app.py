<<<<<<< HEAD
import streamlit as st
import pandas as pd
import base64

from main import generate_pitch_deck
from pdf_reader import extract_pdf_text
from document_search import search_documents


# PAGE CONFIG

st.set_page_config(

    page_title="Investment Banking Intelligence Platform",

    layout="wide"
)


# BACKGROUND IMAGE

def get_base64(file_path):

    with open(file_path, "rb") as image_file:

        encoded = base64.b64encode(

            image_file.read()

        ).decode()

    return encoded


bg_image = get_base64(

    "background.jpg"
)


# CUSTOM CSS

st.markdown(

    f"""

    <style>

    .stApp {{

        background-image:

        linear-gradient(
            rgba(0,0,0,0.82),
            rgba(0,0,0,0.82)
        ),

        url("data:image/jpg;base64,{bg_image}");

        background-size: cover;

        background-position: center;

        background-attachment: fixed;
    }}


    h1, h2, h3, h4, h5, h6,
    p, label, div {{

        color: white !important;
    }}


    .stButton>button {{

        background-color: #3498db;

        color: white;

        border-radius: 10px;

        height: 3em;

        width: 100%;

        font-size: 16px;

        border: none;
    }}


    .stTextInput div div input {{

        background-color: rgba(
            255,
            255,
            255,
            0.08
        ) !important;

        color: white !important;
    }}


    .stMultiSelect div {{

        background-color: rgba(
            255,
            255,
            255,
            0.08
        ) !important;

        color: white !important;
    }}

    </style>

    """,

    unsafe_allow_html=True
)


# TITLE

st.title(

    "Investment Banking Intelligence Platform"
)

st.markdown(

    "Generate institutional-grade investment banking decks automatically."
)


# INPUTS

company_name = st.text_input(

    "Enter Company Name"
)


uploaded_file = st.file_uploader(

    "Upload Annual Report PDF (Optional)",

    type=["pdf"]
)


# SECTION SELECTION

selected_sections = st.multiselect(

    "Select Sections",

    [

        "Executive Dashboard",

        "Company Overview",

        "Business Model",

        "Industry Overview",

        "Financial Performance",

        "Competitor Analysis",

        "Operational Metrics",

        "SWOT Analysis",

        "Risks",

        "Investment Thesis"
    ],

    default=[

        "Executive Dashboard",

        "Company Overview",

        "Financial Performance",

        "SWOT Analysis",

        "Investment Thesis"
    ]
)


# MANUAL OVERRIDES

st.subheader(

    "Manual Override Inputs"
)

manual_aum = st.text_input(

    "AUM"
)

manual_branches = st.text_input(

    "Branches"
)

manual_gnpa = st.text_input(

    "GNPA"
)

manual_roa = st.text_input(

    "ROA"
)


# GENERATE BUTTON

if st.button(

    "Generate Investment Deck"
):


    if company_name or uploaded_file:


        with st.spinner(

            "Generating institutional investment deck..."
        ):


            raw_text = ""


            # COMPANY SEARCH MODE

            if company_name:

                raw_text += f"""

                {company_name} is an India-focused
                corporate entity.

                The company operates across scalable
                business verticals and focuses on
                long-term operational growth.

                """


            # SEARCH DOCUMENTS

            if company_name:

                document_links = search_documents(

                    company_name
                )

                st.subheader(

                    "Discovered Documents"
                )

                for link in document_links:

                    st.write(link)


            # PDF ENRICHMENT MODE

            if uploaded_file is not None:

                try:

                    pdf_text = extract_pdf_text(

                        uploaded_file
                    )

                    raw_text += pdf_text

                except Exception as e:

                    st.warning(

                        f"PDF extraction failed: {e}"
                    )


            # GENERATE ANALYSIS

            result = generate_pitch_deck(

                company_name,

                raw_text,

                selected_sections
            )


            analysis = result["analysis"]

            ppt_path = result["ppt_path"]


            # MANUAL OVERRIDES

            if manual_aum:

                analysis["aum"] = manual_aum


            if manual_branches:

                analysis["branch_count"] = manual_branches


            if manual_gnpa:

                analysis[
                    "financial_performance"
                ]["GNPA"] = manual_gnpa


            if manual_roa:

                analysis[
                    "financial_performance"
                ]["ROA"] = manual_roa


        st.success(

            "Investment deck generated successfully"
        )


        # KPI CARDS

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(

            "AUM / Market Cap",

            analysis["aum"]
        )

        col2.metric(

            "Branches",

            analysis["branch_count"]
        )

        col3.metric(

            "Customers",

            analysis["customer_count"]
        )

        col4.metric(

            "Credit Rating",

            analysis["credit_rating"]
        )


        # TABS

        tab1, tab2, tab3, tab4 = st.tabs([

            "Overview",

            "Financials",

            "Operations",

            "Advisory"
        ])


        # OVERVIEW TAB

        with tab1:

            st.subheader(

                "Company Overview"
            )

            st.write(

                analysis["company_overview"]
            )


            st.subheader(

                "Business Model"
            )

            st.write(

                analysis["business_model"]
            )


            st.subheader(

                "Industry Overview"
            )

            st.write(

                analysis["industry_overview"]
            )


        # FINANCIAL TAB

        with tab2:

            financial_df = pd.DataFrame({

                "Metric":

                list(

                    analysis[
                        "financial_performance"
                    ].keys()
                ),

                "Value":

                list(

                    analysis[
                        "financial_performance"
                    ].values()
                )
            })

            st.dataframe(

                financial_df,

                use_container_width=True
            )


        # OPERATIONS TAB

        with tab3:

            ops_df = pd.DataFrame({

                "Metric": [

                    "AUM / Market Cap",

                    "Branches",

                    "Customers",

                    "Employees"
                ],

                "Value": [

                    analysis["aum"],

                    analysis["branch_count"],

                    analysis["customer_count"],

                    analysis["employee_count"]
                ]
            })

            st.dataframe(

                ops_df,

                use_container_width=True
            )


        # ADVISORY TAB

        with tab4:

            st.subheader(

                "Investment Thesis"
            )

            st.write(

                analysis["investment_thesis"]
            )


            st.subheader(

                "Key Risks"
            )

            for risk in analysis["risks"]:

                st.markdown(

                    f"- {risk}"
                )


        # DOWNLOAD BUTTON

        with open(

            ppt_path,

            "rb"
        ) as file:

            st.download_button(

                label="Download Investment Deck",

                data=file,

                file_name=ppt_path
            )


    else:

        st.error(

            "Please enter company name or upload annual report."
=======
import streamlit as st
import pandas as pd
import base64

from main import generate_pitch_deck
from pdf_reader import extract_pdf_text
from document_search import search_documents


# PAGE CONFIG

st.set_page_config(

    page_title="Investment Banking Intelligence Platform",

    layout="wide"
)


# BACKGROUND IMAGE

def get_base64(file_path):

    with open(file_path, "rb") as image_file:

        encoded = base64.b64encode(

            image_file.read()

        ).decode()

    return encoded


bg_image = get_base64(

    "background.jpg"
)


# CUSTOM CSS

st.markdown(

    f"""

    <style>

    .stApp {{

        background-image:

        linear-gradient(
            rgba(0,0,0,0.82),
            rgba(0,0,0,0.82)
        ),

        url("data:image/jpg;base64,{bg_image}");

        background-size: cover;

        background-position: center;

        background-attachment: fixed;
    }}


    h1, h2, h3, h4, h5, h6,
    p, label, div {{

        color: white !important;
    }}


    .stButton>button {{

        background-color: #3498db;

        color: white;

        border-radius: 10px;

        height: 3em;

        width: 100%;

        font-size: 16px;

        border: none;
    }}


    .stTextInput div div input {{

        background-color: rgba(
            255,
            255,
            255,
            0.08
        ) !important;

        color: white !important;
    }}


    .stMultiSelect div {{

        background-color: rgba(
            255,
            255,
            255,
            0.08
        ) !important;

        color: white !important;
    }}

    </style>

    """,

    unsafe_allow_html=True
)


# TITLE

st.title(

    "Investment Banking Intelligence Platform"
)

st.markdown(

    "Generate institutional-grade investment banking decks automatically."
)


# INPUTS

company_name = st.text_input(

    "Enter Company Name"
)


uploaded_file = st.file_uploader(

    "Upload Annual Report PDF (Optional)",

    type=["pdf"]
)


# SECTION SELECTION

selected_sections = st.multiselect(

    "Select Sections",

    [

        "Executive Dashboard",

        "Company Overview",

        "Business Model",

        "Industry Overview",

        "Financial Performance",

        "Competitor Analysis",

        "Operational Metrics",

        "SWOT Analysis",

        "Risks",

        "Investment Thesis"
    ],

    default=[

        "Executive Dashboard",

        "Company Overview",

        "Financial Performance",

        "SWOT Analysis",

        "Investment Thesis"
    ]
)


# MANUAL OVERRIDES

st.subheader(

    "Manual Override Inputs"
)

manual_aum = st.text_input(

    "AUM"
)

manual_branches = st.text_input(

    "Branches"
)

manual_gnpa = st.text_input(

    "GNPA"
)

manual_roa = st.text_input(

    "ROA"
)


# GENERATE BUTTON

if st.button(

    "Generate Investment Deck"
):


    if company_name or uploaded_file:


        with st.spinner(

            "Generating institutional investment deck..."
        ):


            raw_text = ""


            # COMPANY SEARCH MODE

            if company_name:

                raw_text += f"""

                {company_name} is an India-focused
                corporate entity.

                The company operates across scalable
                business verticals and focuses on
                long-term operational growth.

                """


            # SEARCH DOCUMENTS

            if company_name:

                document_links = search_documents(

                    company_name
                )

                st.subheader(

                    "Discovered Documents"
                )

                for link in document_links:

                    st.write(link)


            # PDF ENRICHMENT MODE

            if uploaded_file is not None:

                try:

                    pdf_text = extract_pdf_text(

                        uploaded_file
                    )

                    raw_text += pdf_text

                except Exception as e:

                    st.warning(

                        f"PDF extraction failed: {e}"
                    )


            # GENERATE ANALYSIS

            result = generate_pitch_deck(

                company_name,

                raw_text,

                selected_sections
            )


            analysis = result["analysis"]

            ppt_path = result["ppt_path"]


            # MANUAL OVERRIDES

            if manual_aum:

                analysis["aum"] = manual_aum


            if manual_branches:

                analysis["branch_count"] = manual_branches


            if manual_gnpa:

                analysis[
                    "financial_performance"
                ]["GNPA"] = manual_gnpa


            if manual_roa:

                analysis[
                    "financial_performance"
                ]["ROA"] = manual_roa


        st.success(

            "Investment deck generated successfully"
        )


        # KPI CARDS

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(

            "AUM / Market Cap",

            analysis["aum"]
        )

        col2.metric(

            "Branches",

            analysis["branch_count"]
        )

        col3.metric(

            "Customers",

            analysis["customer_count"]
        )

        col4.metric(

            "Credit Rating",

            analysis["credit_rating"]
        )


        # TABS

        tab1, tab2, tab3, tab4 = st.tabs([

            "Overview",

            "Financials",

            "Operations",

            "Advisory"
        ])


        # OVERVIEW TAB

        with tab1:

            st.subheader(

                "Company Overview"
            )

            st.write(

                analysis["company_overview"]
            )


            st.subheader(

                "Business Model"
            )

            st.write(

                analysis["business_model"]
            )


            st.subheader(

                "Industry Overview"
            )

            st.write(

                analysis["industry_overview"]
            )


        # FINANCIAL TAB

        with tab2:

            financial_df = pd.DataFrame({

                "Metric":

                list(

                    analysis[
                        "financial_performance"
                    ].keys()
                ),

                "Value":

                list(

                    analysis[
                        "financial_performance"
                    ].values()
                )
            })

            st.dataframe(

                financial_df,

                use_container_width=True
            )


        # OPERATIONS TAB

        with tab3:

            ops_df = pd.DataFrame({

                "Metric": [

                    "AUM / Market Cap",

                    "Branches",

                    "Customers",

                    "Employees"
                ],

                "Value": [

                    analysis["aum"],

                    analysis["branch_count"],

                    analysis["customer_count"],

                    analysis["employee_count"]
                ]
            })

            st.dataframe(

                ops_df,

                use_container_width=True
            )


        # ADVISORY TAB

        with tab4:

            st.subheader(

                "Investment Thesis"
            )

            st.write(

                analysis["investment_thesis"]
            )


            st.subheader(

                "Key Risks"
            )

            for risk in analysis["risks"]:

                st.markdown(

                    f"- {risk}"
                )


        # DOWNLOAD BUTTON

        with open(

            ppt_path,

            "rb"
        ) as file:

            st.download_button(

                label="Download Investment Deck",

                data=file,

                file_name=ppt_path
            )


    else:

        st.error(

            "Please enter company name or upload annual report."
>>>>>>> 7282c85c385b2a4b5aa442fe1580cf10806353da
        )