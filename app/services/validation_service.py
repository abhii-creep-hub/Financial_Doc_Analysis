def validate_invoice(data):
    validation = {
        "status": "Valid",
        "calculated_subtotal": 0.0,
        "errors": []
    }

    try:
        
        total = float(data.get("total_amount") or 0)
        tax = float(data.get("tax_amount") or 0)

        
        subtotal = total - tax
        validation["calculated_subtotal"] = round(subtotal, 2)

       
        if not data.get("invoice_number"):
            validation["errors"].append("Missing Invoice Number")

        if not data.get("invoice_date"):
            validation["errors"].append("Missing Invoice Date")

        if not data.get("vendor_name"):
            validation["errors"].append("Missing Vendor Name")

      
        if total <= 0:
            validation["errors"].append("Invalid Total Amount")

        if tax < 0:
            validation["errors"].append("Invalid Tax Amount")

        if subtotal < 0:
            validation["errors"].append("Subtotal cannot be negative")

        
        if validation["errors"]:
            validation["status"] = "Invalid"

        return validation

    except Exception as e:
        return {
            "status": "Error",
            "calculated_subtotal": 0.0,
            "errors": [str(e)]
        }