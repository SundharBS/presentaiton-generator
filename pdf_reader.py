import pdfplumber


def extract_pdf_text(uploaded_file):

    text = ""

    try:

        uploaded_file.seek(0)

        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                try:

                    page_text = page.extract_text()

                    if page_text:
                        text += page_text + "\n"

                except:
                    pass

    except:
        pass

    return text