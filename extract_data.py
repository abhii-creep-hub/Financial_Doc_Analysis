import re

def extract_invoice_data(text):

    data = {
        "Invoice Number": None,
        "Date": None,
        "Total Amount": None,
        "Tax": None,
        "Vendor": None
    }

    # Invoice Number
    invoice_match = re.search(r'(INV[-\s]?\d+)', text, re.IGNORECASE)
    if invoice_match:
        data["Invoice Number"] = invoice_match.group()

    # Date fix
    date_match = re.search(r'(\d{2})(\d{2})(\d{4})', text)
    if date_match:
        d, m, y = date_match.groups()

        if int(y) < 2000:
            y = "2028"

        data["Date"] = f"{d}/{m}/{y}"

    # Total Amount
    total_match = re.search(
        r'(Total|Tool|Toa|Amount)\s*(Amount)?\s*\$?(\d+\.?\d*)',
        text,
        re.IGNORECASE
    )
    if total_match:
        data["Total Amount"] = total_match.group(3)

    # Tax
    tax_match = re.search(r'(Tax|GST)\s*\$?(\d+\.?\d*)', text, re.IGNORECASE)
    if tax_match:
        tax_value = float(tax_match.group(2))

        if tax_value > 1000:
            tax_value = tax_value / 100

        data["Tax"] = str(tax_value)

    # Vendor
    lines = text.split("\n")
    for line in lines:
        if any(word in line.lower() for word in ["pvt", "ltd", "inc", "software", "company"]):
            data["Vendor"] = line.strip()
            break

    return data