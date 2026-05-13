import pdfplumber
import pytesseract

from pdf2image import convert_from_bytes


pytesseract.pytesseract.tesseract_cmd = (

    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_pdf_text(uploaded_file):

    text = ""


    try:

        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:

                    text += page_text

    except:

        pass


    if len(text) < 1000:

        uploaded_file.seek(0)

        images = convert_from_bytes(

            uploaded_file.read(),

            poppler_path=r"C:\poppler\Library\bin"
        )


        for image in images[:15]:

            text += pytesseract.image_to_string(

                image
            )


    return text