import csv
import os

FILE_PATH = "invoice_database.csv"


def save_invoice(data):
    try:
        file_exists = os.path.isfile(FILE_PATH)

        # --- CLEAN DATA BEFORE SAVING ---
        cleaned_data = {
            "invoice_number": str(data.get("invoice_number") or "").strip(),
            "invoice_date": str(data.get("invoice_date") or "").strip(),
            "vendor_name": str(data.get("vendor_name") or "Unknown").strip(),
            "total_amount": float(data.get("total_amount") or 0),
            "tax_amount": float(data.get("tax_amount") or 0)
        }

        with open(FILE_PATH, "a", newline="", encoding="utf-8") as file:
            fieldnames = [
                "invoice_number",
                "invoice_date",
                "vendor_name",
                "total_amount",
                "tax_amount"
            ]

            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # --- WRITE HEADER ONLY ONCE ---
            if not file_exists:
                writer.writeheader()

            writer.writerow(cleaned_data)

        print("Invoice saved successfully")

    except Exception as e:
        print("Error saving invoice:", str(e))