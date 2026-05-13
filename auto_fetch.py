import os
import requests

from duckduckgo_search import DDGS


def find_company_documents(company_name):

    queries = [

        f"{company_name} annual report pdf",

        f"{company_name} investor presentation pdf",

        f"{company_name} credit rating pdf"
    ]

    pdf_links = []

    try:

        with DDGS() as ddgs:

            for query in queries:

                results = ddgs.text(

                    query,

                    max_results=5
                )

                for result in results:

                    url = result.get(

                        "href",

                        ""
                    )

                    if ".pdf" in url.lower():

                        pdf_links.append(url)

    except:
        pass

    return list(set(pdf_links))


def download_company_documents(

    company_name,
    pdf_links
):

    company_folder = os.path.join(

        "documents",

        company_name
    )

    os.makedirs(

        company_folder,

        exist_ok=True
    )

    downloaded_files = []

    for index, url in enumerate(pdf_links):

        try:

            response = requests.get(

                url,

                timeout=20
            )

            file_path = os.path.join(

                company_folder,

                f"document_{index+1}.pdf"
            )

            with open(file_path, "wb") as file:

                file.write(response.content)

            downloaded_files.append(file_path)

        except:
            pass

    return downloaded_files