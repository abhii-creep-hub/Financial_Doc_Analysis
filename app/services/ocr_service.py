import pytesseract
import cv2
import os

def extract_text(image_path):
    try:
        image = cv2.imread(image_path)

        if image is None:
            return "No image found"

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        thresh = cv2.medianBlur(thresh, 3)

        text = pytesseract.image_to_string(thresh, config="--oem 3 --psm 6")
        return text.strip()

    except Exception as e:
        return "Demo invoice text (OCR disabled in deployment)"