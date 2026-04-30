import pytesseract
import cv2
import os

# Set Tesseract path only for Windows
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"Image not found or unable to read: {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    text = pytesseract.image_to_string(thresh)
    return text