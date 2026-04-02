import os
from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename

from app.services.ocr_service import extract_text
from app.services.extraction_service import extract_invoice_data
from app.services.validation_service import validate_invoice
from app.services.fraud_service import detect_fraud
from app.services.analytics_service import save_invoice

main = Blueprint('main', __name__)

UPLOAD_FOLDER = "app/uploads"


@main.route('/')
def home():
    return render_template('index.html')


@main.route('/upload', methods=['POST'])
def upload_file():
    if 'invoice_file' not in request.files:
        return "No file uploaded"

    file = request.files['invoice_file']

    if file.filename == '':
        return "No selected file"

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    text = extract_text(filepath)
    data = extract_invoice_data(text)
    validation = validate_invoice(data)
    fraud_result = detect_fraud(data)

    save_invoice(data)

    return render_template(
        'result.html',
        invoice_data=data,
        validation_result=validation,
        fraud_result=fraud_result,
        extracted_text=text
    )