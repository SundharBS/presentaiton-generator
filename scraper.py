import requests
from bs4 import BeautifulSoup


# COMPANY WEBSITE SCRAPER

def scrape_company_website(url):

    try:

        headers = {

            "User-Agent":

            "Mozilla/5.0"
        }


        response = requests.get(

            url,

            headers=headers,

            timeout=15
        )


        soup = BeautifulSoup(

            response.text,

            "html.parser"
        )


        # REMOVE SCRIPTS

        for script in soup([

            "script",
            "style"
        ]):

            script.decompose()


        text = soup.get_text(

            separator=" "
        )


        cleaned_text = " ".join(

            text.split()
        )


        return cleaned_text[:50000]


    except Exception as e:

        return f"Scraping Error: {e}"