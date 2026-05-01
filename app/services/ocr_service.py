import requests
import os

API_KEY = os.environ.get("OCR_API_KEY")

def extract_text(image_path):
    try:
        if not API_KEY:
            return "API KEY MISSING"

        with open(image_path, 'rb') as f:
            response = requests.post(
                'https://api.ocr.space/parse/image',
                files={'file': f},
                data={
                    'apikey': API_KEY,
                    'language': 'eng',
                    'OCREngine': 2   # 🔥 IMPORTANT (better accuracy)
                }
            )

        result = response.json()

        # 🔥 show full error
        if result.get("IsErroredOnProcessing"):
            return f"ERROR: {result}"

        text = result['ParsedResults'][0]['ParsedText']

        if not text.strip():
            return "NO TEXT DETECTED"

        return text

    except Exception as e:
        return f"EXCEPTION: {str(e)}"