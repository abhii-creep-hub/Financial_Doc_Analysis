import json
import os
from google.cloud import vision
from google.oauth2 import service_account
import io

def extract_text(image_path):
    try:
        credentials_info = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
        credentials = service_account.Credentials.from_service_account_info(credentials_info)

        client = vision.ImageAnnotatorClient(credentials=credentials)

        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = client.text_detection(image=image)

        if response.text_annotations:
            return response.text_annotations[0].description
        else:
            return "No text detected"

    except Exception as e:
        return str(e)