from ocr_module import extract_text
from extract_data import extract_invoice_data
from validate_data import validate_invoice
from fraud_detection import detect_fraud

file_path = "invoice.png"

# Step 1: OCR
text = extract_text(file_path)

print("OCR Text:")
print(text)

# Step 2: Extract Data
print("\nExtracted Financial Data:")
data = extract_invoice_data(text)

for key, value in data.items():
    print(key, ":", value)

# Step 3: Validation
print("\nValidation Result:")
validation = validate_invoice(data)

for key, value in validation.items():
    print(key, ":", value)

# Step 4: Fraud Detection
print("\nFraud Detection:")
print(detect_fraud(data))