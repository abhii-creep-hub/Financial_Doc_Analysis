import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_entities(text):

    doc = nlp(text)

    data = {
        "Date": None,
        "Vendor": None,
        "Total Amount": None
    }

    for ent in doc.ents:

        if ent.label_ == "DATE":
            data["Date"] = ent.text

        elif ent.label_ == "ORG":
            data["Vendor"] = ent.text

        elif ent.label_ == "MONEY":
            data["Total Amount"] = ent.text

    
    invoice_match = re.search(r'(INV[-\s]?\d+)', text)

    if invoice_match:
        data["Invoice Number"] = invoice_match.group()

    return data