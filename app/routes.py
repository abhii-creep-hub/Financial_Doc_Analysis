import os
import pandas as pd
from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename

from app.services.ocr_service import extract_text
from app.services.extraction_service import extract_invoice_data
from app.services.validation_service import validate_invoice
from app.services.fraud_service import detect_fraud
from app.services.analytics_service import save_invoice

main = Blueprint('main', __name__)

UPLOAD_FOLDER = "app/uploads"


# ✅ DASHBOARD ROUTE (FINAL FIXED)
@main.route('/dashboard')
def dashboard():
    try:
        df = pd.read_csv("invoice_database.csv")

        # Clean column names
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

        print("Columns:", df.columns)
        print(df.head())

        # Fix vendor column mismatch
        if "vendor_name" not in df.columns:
            if "vendor" in df.columns:
                df.rename(columns={"vendor": "vendor_name"}, inplace=True)
            else:
                return f"Error: vendor column missing. Found: {df.columns}"

        # Check total_amount
        if "total_amount" not in df.columns:
            return f"Error: total_amount column missing. Found: {df.columns}"

        # Convert to numeric
        df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce")

        # Calculations
        total_invoices = len(df)
        total_revenue = df["total_amount"].sum()
        avg_amount = df["total_amount"].mean()

        df = df[df["vendor_name"].notna()]
        df["vendor_name"] = df["vendor_name"].astype(str)
        # remove numeric-only vendors
        df = df[~df["vendor_name"].str.match(r'^\d+(\.\d+)?$')]
        vendor_counts = df["vendor_name"].value_counts().to_dict()

        return render_template(
            "dashboard.html",
            total_invoices=total_invoices,
            total_revenue=round(total_revenue, 2),
            avg_amount=round(avg_amount, 2),
            vendor_counts=vendor_counts
        )

    except Exception as e:
        return f"Error: {str(e)}"


# ✅ HOME ROUTE
@main.route('/')
def home():
    return render_template('index.html')


# ✅ UPLOAD ROUTE
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

    # Processing
    text = extract_text(filepath)
    data = extract_invoice_data(text)
    validation = validate_invoice(data)
    fraud_result = detect_fraud(data)

    # Save to CSV
    save_invoice(data)

    return render_template(
        'result.html',
        invoice_data=data,
        validation_result=validation,
        fraud_result=fraud_result,
        extracted_text=text
    )