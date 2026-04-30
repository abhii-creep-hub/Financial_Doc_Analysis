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

    text = text.replace("\r", "")
    
    # ---------------- INVOICE NUMBER ----------------
    invoice_patterns = [
        r'Invoice\s*(?:No|Number|#)?[:\s]*([A-Z0-9\-\/]{3,})',
        r'INV[\s\-#]*([A-Z0-9\-]{3,})'
    ]

    for pattern in invoice_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            if len(value) >= 3 and not value.isalpha():  # avoid picking words like "URBAN"
                data["invoice_number"] = value
                break

    # ---------------- DATE ----------------
    date_match = re.search(
        r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b',
        text
    )

    if date_match:
        data["invoice_date"] = date_match.group()

    # ---------------- TOTAL AMOUNT ----------------
    total_patterns = [
        r'(Grand\s*Total|Total\s*Amount|Amount\s*Due)[^\d]*([\d,]+\.\d{2})',
        r'Total[^\d]*([\d,]+\.\d{2})'
    ]

    for pattern in total_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amount = match.group(len(match.groups())).replace(',', '')
            try:
                data["total_amount"] = float(amount)
                break
            except:
                pass

    # ---------------- TAX ----------------
    tax_match = re.search(
        r'(GST|Tax)[^\d]*([\d,]+\.\d{2})',
        text,
        re.IGNORECASE
    )

    if tax_match:
        try:
            data["tax_amount"] = float(tax_match.group(2).replace(',', ''))
        except:
            pass

    # ---------------- VENDOR ----------------
    lines = text.split("\n")

    for line in lines[:10]: 
        if any(word in line.lower() for word in ["ltd", "pvt", "inc", "llp"]):
            data["vendor_name"] = line.strip()
            break

    
    doc = nlp(text)

    for ent in doc.ents:
        if not data["invoice_date"] and ent.label_ == "DATE":
            data["invoice_date"] = ent.text

        if not data["vendor_name"] and ent.label_ == "ORG":
            data["vendor_name"] = ent.text

        if not data["total_amount"] and ent.label_ == "MONEY":
            money_text = ent.text.replace("$", "").replace(",", "").strip()
            try:
                value = float(re.sub(r"[^\d.]", "", money_text))
                if value > 10:  
                    data["total_amount"] = value
            except:
                pass

    return data