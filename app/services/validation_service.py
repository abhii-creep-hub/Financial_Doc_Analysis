def validate_invoice(data):
    try:
        total = float(data["total_amount"]) if data["total_amount"] else 0
        tax = float(data["tax_amount"]) if data["tax_amount"] else 0

        subtotal = total - tax

        validation = {
            "calculated_subtotal": round(subtotal, 2),
            "validation_status": "Valid"
        }

        if subtotal < 0:
            validation["validation_status"] = "Invalid Data"

        if not data["invoice_number"] or not data["invoice_date"] or not data["vendor_name"]:
            validation["validation_status"] = "Missing Important Fields"

        return validation

    except:
        return {"validation_status": "Validation Failed"}