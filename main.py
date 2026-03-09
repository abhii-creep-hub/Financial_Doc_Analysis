from ocr_module import extract_text
from extract_data import extract_invoice_data
from validate_data import validate_invoice

file_path = "invoice.png"

text = extract_text(file_path)

print("OCR Text:")
print(text)

print("\nExtracted Financial Data:")

data = extract_invoice_data(text)

for key, value in data.items():
    print(key, ":", value)


print("\nValidation Result:")

validation = validate_invoice(data)

for key, value in validation.items():
    print(key, ":", value)