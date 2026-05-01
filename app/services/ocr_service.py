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
                    'language': 'eng'
                }
            )

        result = response.json()

        if result.get("IsErroredOnProcessing"):
            return str(result)

        text = result['ParsedResults'][0]['ParsedText']
        return text.strip()

    except Exception as e:
        return str(e)