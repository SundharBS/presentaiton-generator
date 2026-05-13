import pdfplumber
import pytesseract

from pdf2image import convert_from_bytes


# TESSERACT PATH

pytesseract.pytesseract.tesseract_cmd = (

    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# MAIN PDF EXTRACTION FUNCTION

def extract_pdf_text(uploaded_file):

    text = ""


    # RESET POINTER

    try:

        uploaded_file.seek(0)

    except:

        pass


    # TRY NORMAL PDF EXTRACTION

    try:

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


    # OCR FALLBACK

    if len(text.strip()) < 1000:

        try:

            uploaded_file.seek(0)

            images = convert_from_bytes(

                uploaded_file.read(),

                poppler_path=r"C:\poppler\Library\bin"
            )


            for image in images[:15]:

                try:

                    extracted = pytesseract.image_to_string(

                        image
                    )

                    text += extracted + "\n"

                except:

                    pass

        except:

            pass


    return text