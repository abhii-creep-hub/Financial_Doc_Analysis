import re

def extract_invoice_data(text):

    data = {
        "Invoice Number": None,
        "Date": None,
        "Total Amount": None,
        "Tax": None,
        "Vendor": None
    }

    invoice_patterns = [
        r'Invoice\s*(?:No|Number|ID)?[:\s#]*([A-Z0-9\-]+)',
        r'INV[#\-\s]*([A-Z0-9\-]+)'
    ]

    for pattern in invoice_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data["Invoice Number"] = match.group(1)
            break

    date_match = re.search(r'(\d{1,2}\s+[A-Za-z]+\s+\d{4})|(\d{1,2}/\d{1,2}/\d{4})', text)

    if date_match:
        data["Date"] = date_match.group()

    total_patterns = [
        r'TOTAL\s*PAYABLE\s*\$?(\d+)',
        r'Amount\s*Due\s*\$?(\d+)',
        r'Total\s*\$?(\d+)'
    ]

    for pattern in total_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data["Total Amount"] = match.group(1)
            break

    tax_match = re.search(r'(Tax|GST)\s*\$?(\d+)', text, re.IGNORECASE)

    if tax_match:
        data["Tax"] = tax_match.group(2)

    lines = text.split("\n")

    for line in lines:
        if "pvt" in line.lower() or "ltd" in line.lower() or "inc" in line.lower():
            data["Vendor"] = line.strip()
            break

    return data