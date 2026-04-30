import easyocr

# initialize once
reader = easyocr.Reader(['en'])

def extract_text(image_path):
    try:
        result = reader.readtext(image_path, detail=0)
        text = " ".join(result)
        return text
    except Exception as e:
        return "OCR failed"