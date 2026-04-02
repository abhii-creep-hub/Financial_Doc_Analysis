import os
import cv2
import pytesseract
import pdfplumber

# Path to Tesseract OCR executable (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(file_path):
    """
    Extract text from an invoice file.
    Supports both image files and PDFs.
    """

    file_extension = os.path.splitext(file_path)[1].lower()

    # If the file is an image
    if file_extension in ['.png', '.jpg', '.jpeg']:
        return extract_text_from_image(file_path)

    # If the file is a PDF
    elif file_extension == '.pdf':
        return extract_text_from_pdf(file_path)

    else:
        return "Unsupported file format"


def extract_text_from_image(image_path):
    """
    Extract text from image using OCR.
    """

    image = cv2.imread(image_path)

    if image is None:
        return "Could not read image"

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    text = pytesseract.image_to_string(thresh)
    return text


def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF using pdfplumber.
    """

    extracted_text = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n"

    except Exception as e:
        return f"Error reading PDF: {str(e)}"

    return extracted_text