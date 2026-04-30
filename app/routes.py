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


# ---------------- HOME ----------------
@main.route('/')
def home():
    return render_template('index.html')


# ---------------- DASHBOARD ----------------
@main.route('/dashboard')
def dashboard():
    try:
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

        if df.empty:
            return render_template(
                "dashboard.html",
                total_invoices=0,
                total_revenue=0,
                avg_amount=0,
                vendor_counts={},
                monthly_data={}
            )

        # --- CLEAN COLUMNS ---
        df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]

        # --- HANDLE MISSING COLUMNS ---
        if "vendor_name" not in df.columns:
            df["vendor_name"] = "Unknown"

        if "total_amount" not in df.columns:
            df["total_amount"] = 0

        # --- TYPE CONVERSION ---
        df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce").fillna(0)
        df["vendor_name"] = df["vendor_name"].fillna("Unknown").astype(str)

        # --- CLEAN DATA ---
        df = df[~df["vendor_name"].str.match(r'^\d+(\.\d+)?$', na=False)]

        # --- METRICS ---
        total_invoices = int(len(df))
        total_revenue = float(df["total_amount"].sum())
        avg_amount = float(df["total_amount"].mean()) if total_invoices > 0 else 0

        vendor_counts = df["vendor_name"].value_counts().to_dict()

        # --- MONTHLY ANALYTICS ---
        monthly_data = {}
        if "invoice_date" in df.columns:
            try:
                df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")
                df_valid = df.dropna(subset=["invoice_date"])

                if not df_valid.empty:
                    monthly_data = (
                        df_valid.groupby(df_valid["invoice_date"].dt.month)["total_amount"]
                        .sum()
                        .to_dict()
                    )
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
        print("Dashboard ERROR:", e)
        return f"Dashboard Error: {str(e)}"


# ---------------- UPLOAD ----------------
@main.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'invoice_file' not in request.files:
            return "No file uploaded"

        file = request.files['invoice_file']

        if file.filename == '':
            return "No selected file"

        # --- FILE VALIDATION ---
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return "Invalid file type"

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # --- PIPELINE ---
        text = extract_text(filepath)

        if not text.strip():
            return "OCR failed. Try clearer image."

        data = extract_invoice_data(text)

        validation = validate_invoice(data)

        fraud_result = detect_fraud(data)

        save_invoice(data)

        print("Invoice processed successfully")

        return render_template(
            'result.html',
            invoice_data=data,
            validation_result=validation,
            fraud_result=fraud_result,
            extracted_text=text
        )

    except Exception as e:
        print("Upload ERROR:", e)
        return f"Upload Error: {str(e)}"