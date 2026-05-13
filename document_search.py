<<<<<<< HEAD
from googlesearch import search


def search_documents(company_name):

    queries = [

        f"{company_name} annual report pdf",

        f"{company_name} investor presentation pdf",

        f"{company_name} credit rating pdf",

        f"{company_name} CARE rating pdf",

        f"{company_name} CRISIL rating pdf",

        f"{company_name} ICRA rating pdf"
    ]


    results = []


    for query in queries:

        try:

            for url in search(

                query,

                num_results=2
            ):

                if ".pdf" in url:

                    results.append(url)

        except:

            pass


=======
from googlesearch import search


def search_documents(company_name):

    queries = [

        f"{company_name} annual report pdf",

        f"{company_name} investor presentation pdf",

        f"{company_name} credit rating pdf",

        f"{company_name} CARE rating pdf",

        f"{company_name} CRISIL rating pdf",

        f"{company_name} ICRA rating pdf"
    ]


    results = []


    for query in queries:

        try:

            for url in search(

                query,

                num_results=2
            ):

                if ".pdf" in url:

                    results.append(url)

        except:

            pass


>>>>>>> 7282c85c385b2a4b5aa442fe1580cf10806353da
    return list(set(results))