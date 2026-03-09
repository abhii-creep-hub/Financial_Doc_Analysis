def validate_invoice(data):
    
    try:
        total = float(data["Total Amount"]) if data["Total Amount"] else 0
        tax = float(data["Tax"]) if data["Tax"] else 0
        
        subtotal = total - tax
        
        validation = {
            "Calculated Subtotal": round(subtotal, 2),
            "Validation Status": "Valid"
        }

        if subtotal < 0:
            validation["Validation Status"] = "Invalid Data"

        return validation

    except:
        return {"Validation Status": "Validation Failed"}