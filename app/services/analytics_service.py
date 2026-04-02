import csv
import os

def save_invoice(data):
    file_path = "invoice_database.csv"
    file_exists = os.path.isfile(file_path)

    with open(file_path, "a", newline="", encoding="utf-8") as file:
        fieldnames = ["invoice_number", "invoice_date", "vendor_name", "total_amount", "tax_amount"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "invoice_number": data.get("invoice_number"),
            "invoice_date": data.get("invoice_date"),
            "vendor_name": data.get("vendor_name"),
            "total_amount": data.get("total_amount"),
            "tax_amount": data.get("tax_amount")
        })