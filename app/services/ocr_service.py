import requests

API_KEY = "K83791192288957"

def extract_text(image_path):
    try:
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

        if result['IsErroredOnProcessing']:
            return "OCR failed"

        text = result['ParsedResults'][0]['ParsedText']
        return text.strip()

    except Exception as e:
        return "OCR failed"