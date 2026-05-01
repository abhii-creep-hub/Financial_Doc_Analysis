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
        r'Invoice\s*Number\s*[:\-]?\s*(INV[-\d]+)',
        r'\b(INV[-\d]{3,})\b'
    ]

    for pattern in invoice_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data["invoice_number"] = match.group(1)
            break

    # ---------------- DATE ----------------
    date_match = re.search(
        r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}',
        text
    )

    if date_match:
        data["invoice_date"] = date_match.group()

    # ---------------- TOTAL (FIXED) ----------------
    # Priority: Total Due / Grand Total / last Total
    total_patterns = [
        r'(Total\s*Due|Grand\s*Total)[^\d]*([\d]+\.\d{2})',
        r'Total[^\d]*([\d]+\.\d{2})'
    ]

    for pattern in total_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            value = matches[-1]  # take LAST total (important)
            amount = value[-1] if isinstance(value, tuple) else value
            try:
                data["total_amount"] = float(amount)
                break
            except:
                pass

    # ---------------- TAX (FIXED) ----------------
    tax_match = re.search(
        r'(Tax|GST)[^\d]*([\d]+\.\d{2})',
        text,
        re.IGNORECASE
    )

    if tax_match:
        try:
            data["tax_amount"] = float(tax_match.group(2))
        except:
            pass

    # ---------------- VENDOR ----------------
    lines = text.split("\n")

    for i, line in enumerate(lines):
        if "from:" in line.lower():
            if i + 1 < len(lines):
                data["vendor_name"] = lines[i + 1].strip()
                break

    # ---------------- NLP FALLBACK ----------------
    doc = nlp(text)

    for ent in doc.ents:

        if not data["invoice_date"] and ent.label_ == "DATE":
            data["invoice_date"] = ent.text

        if not data["vendor_name"] and ent.label_ == "ORG":
            data["vendor_name"] = ent.text

        if not data["total_amount"] and ent.label_ == "MONEY":
            try:
                value = float(re.sub(r"[^\d.]", "", ent.text))
                if value > 10:
                    data["total_amount"] = value
            except:
                pass

    return data