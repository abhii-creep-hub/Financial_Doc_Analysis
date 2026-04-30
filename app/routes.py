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


@main.route('/')
def home():
    return render_template('index.html')


@main.route('/dashboard')
def dashboard():
    try:
        # If file not exists
        if not os.path.exists("invoice_database.csv"):
            return render_template(
                "dashboard.html",
                total_invoices=0,
                total_revenue=0,
                avg_amount=0,
                vendor_counts={},
                monthly_data={}
            )

        df = pd.read_csv("invoice_database.csv")

        # If CSV empty
        if df.empty:
            return render_template(
                "dashboard.html",
                total_invoices=0,
                total_revenue=0,
                avg_amount=0,
                vendor_counts={},
                monthly_data={}
            )

        # Clean column names
        df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]

        # Fix missing columns
        if "vendor_name" not in df.columns:
            if "vendor" in df.columns:
                df.rename(columns={"vendor": "vendor_name"}, inplace=True)
            else:
                df["vendor_name"] = "Unknown"

        if "total_amount" not in df.columns:
            df["total_amount"] = 0

        # Convert data
        df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce").fillna(0)
        df["vendor_name"] = df["vendor_name"].fillna("Unknown").astype(str)

        # Remove invalid vendor names
        df = df[~df["vendor_name"].str.match(r'^\d+(\.\d+)?$', na=False)]

        # Stats
        total_invoices = len(df)
        total_revenue = df["total_amount"].sum()
        avg_amount = df["total_amount"].mean() if total_invoices > 0 else 0

        # Vendor counts
        vendor_counts = df["vendor_name"].value_counts().to_dict() or {}

        # Monthly data
        monthly_data = {}
        if "invoice_date" in df.columns:
            try:
                df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")
                df_valid = df.dropna(subset=["invoice_date"])
                if not df_valid.empty:
                    monthly_data = df_valid.groupby(
                        df_valid["invoice_date"].dt.month
                    )["total_amount"].sum().to_dict()
            except Exception:
                monthly_data = {}

        return render_template(
            "dashboard.html",
            total_invoices=total_invoices,
            total_revenue=round(total_revenue, 2),
            avg_amount=round(avg_amount, 2),
            vendor_counts=vendor_counts,
            monthly_data=monthly_data
        )

    except Exception as e:
        print("ERROR:", e)
        return f"Error: {str(e)}"


@main.route('/upload', methods=['POST'])
def upload_file():
    if 'invoice_file' not in request.files:
        return "No file uploaded"

    file = request.files['invoice_file']

    if file.filename == '':
        return "No selected file"

    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # 🔥 OCR + processing
    text = extract_text(filepath)
    data = extract_invoice_data(text)
    validation = validate_invoice(data)
    fraud_result = detect_fraud(data)

    # Save to CSV
    save_invoice(data)

    # ✅ RETURN RESULT PAGE (CORRECT FLOW)
    return render_template(
        'result.html',
        invoice_data=data,
        validation_result=validation,
        fraud_result=fraud_result,
        extracted_text=text
    )