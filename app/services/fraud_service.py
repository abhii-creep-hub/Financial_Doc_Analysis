from sklearn.ensemble import IsolationForest
import pandas as pd

sample_data = pd.DataFrame({
    "total_amount": [500, 620, 610, 590, 605, 615, 600, 598],
    "tax": [20, 21, 21, 20, 21, 21, 20, 20]
})

model = IsolationForest(contamination=0.1, random_state=42)
model.fit(sample_data)

def detect_fraud(data):
    try:
        total = float(data["total_amount"]) if data["total_amount"] else 0
        tax = float(data["tax_amount"]) if data["tax_amount"] else 0

        test_df = pd.DataFrame({
            "total_amount": [total],
            "tax": [tax]
        })

        prediction = model.predict(test_df)

        if prediction[0] == -1:
            return "Suspicious Invoice Detected"
        else:
            return "Invoice Looks Normal"

    except:
        return "Fraud detection failed"