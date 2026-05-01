import requests
import os

API_KEY = os.environ.get("OCR_API_KEY")

def extract_text(image_path):
    try:
        if not API_KEY:
            return "ERROR: API key missing"

        with open(image_path, 'rb') as f:
            response = requests.post(
                'https://api.ocr.space/parse/image',
                files={'file': f},
                data={
                    'apikey': API_KEY,
                    'language': 'eng',
                    'OCREngine': 2
                }
            )

        result = response.json()

        # 🔥 Check if API returned error
        if result.get("IsErroredOnProcessing"):
            return f"OCR API ERROR: {result.get('ErrorMessage')}"

        # 🔥 Safe access
        parsed = result.get("ParsedResults")
        if not parsed:
            return f"OCR RESPONSE ERROR: {result}"

        text = parsed[0].get("ParsedText", "")

        if not text.strip():
            return "NO TEXT DETECTED"

        return text.strip()

    except Exception as e:
        return f"EXCEPTION: {str(e)}"