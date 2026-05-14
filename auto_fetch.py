from duckduckgo_search import DDGS


def fetch_company_data(company_name):

    query = f"{company_name} company overview financials business model"

    results_text = ""

    try:

        with DDGS() as ddgs:

            results = ddgs.text(
                query,
                max_results=10
            )

            for result in results:

                title = result.get("title", "")
                body = result.get("body", "")

                results_text += f"{title}\n{body}\n\n"

    except Exception as e:

        results_text = f"Error fetching company data: {str(e)}"

    return results_text