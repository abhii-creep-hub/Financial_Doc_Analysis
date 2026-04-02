import re
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_invoice_data(text):
    data = {
        "invoice_number": None,
        "invoice_date": None,
        "total_amount": None,
        "tax_amount": None,
        "vendor_name": None
    }

    invoice_patterns = [
        r'Invoice\s*(?:No|Number|ID)?[:\s#]*([A-Z0-9\-]+)',
        r'INV[#\-\s]*([A-Z0-9\-]+)'
    ]

    for pattern in invoice_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data["invoice_number"] = match.group(1)
            break

    date_match = re.search(
        r'(\d{1,2}\s+[A-Za-z]+\s+\d{4})|(\d{1,2}/\d{1,2}/\d{4})',
        text
    )

    if date_match:
        data["invoice_date"] = date_match.group()

    total_patterns = [
        r'TOTAL\s*PAYABLE\s*\$?\s*([\d,]+(?:\.\d{2})?)',
        r'Amount\s*Due\s*\$?\s*([\d,]+(?:\.\d{2})?)',
        r'Total\s*\$?\s*([\d,]+(?:\.\d{2})?)'
    ]

    for pattern in total_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amount = match.group(1).replace(',', '').strip()
            try:
                data["total_amount"] = float(amount)
            except ValueError:
                pass
            break

    tax_match = re.search(
        r'(Tax|GST)\s*\$?\s*([\d,]+(?:\.\d{2})?)',
        text,
        re.IGNORECASE
    )

    if tax_match:
        tax_value = tax_match.group(2).replace(',', '').strip()
        try:
            data["tax_amount"] = float(tax_value)
        except ValueError:
            pass

    lines = text.split("\n")

    for line in lines:
        if "pvt" in line.lower() or "ltd" in line.lower() or "inc" in line.lower():
            data["vendor_name"] = line.strip()
            break

    doc = nlp(text)

    for ent in doc.ents:
        if not data["invoice_date"] and ent.label_ == "DATE":
            data["invoice_date"] = ent.text

        elif not data["vendor_name"] and ent.label_ == "ORG":
            data["vendor_name"] = ent.text

        elif not data["total_amount"] and ent.label_ == "MONEY":
            money_text = ent.text.replace("$", "").replace(",", "").strip()
            try:
                data["total_amount"] = float(money_text)
            except ValueError:
                pass

    return data