from sklearn.ensemble import IsolationForest
import pandas as pd

# Sample training data (normal invoices)
sample_data = pd.DataFrame({
    "total_amount": [500, 620, 610, 590, 605, 615, 600, 598],
    "tax": [20, 21, 21, 20, 21, 21, 20, 20]
})

# Train model
model = IsolationForest(contamination=0.1)
model.fit(sample_data)


def detect_fraud(data):

    try:
        if not data["Total Amount"] or not data["Tax"]:
            return "Insufficient data for fraud detection"

        total = float(data["Total Amount"])
        tax = float(data["Tax"])

        test_df = pd.DataFrame({
            "total_amount": [total],
            "tax": [tax]
        })

        prediction = model.predict(test_df)

        if prediction[0] == -1:
            return "Suspicious Invoice Detected"
        else:
            return "Invoice Looks Normal"

    except Exception as e:
        return f"Fraud detection failed: {e}"