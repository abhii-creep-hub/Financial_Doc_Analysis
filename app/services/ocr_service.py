import pytesseract
import cv2
import os


# Windows support (local system)
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"Image not found or unable to read: {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Improve OCR accuracy
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Optional: denoise
    thresh = cv2.medianBlur(thresh, 3)

    # OCR extraction
    text = pytesseract.image_to_string(thresh, config="--oem 3 --psm 6")

    return text.strip()