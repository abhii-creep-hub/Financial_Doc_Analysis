from sklearn.ensemble import IsolationForest
import pandas as pd


sample_data = pd.DataFrame({
    "total_amount": [500, 620, 610, 590, 605, 615, 600, 598],
    "tax": [20, 21, 21, 20, 21, 21, 20, 20]
})

model = IsolationForest(contamination=0.1, random_state=42)
model.fit(sample_data)


def detect_fraud(data):
    result = {
        "status": "Normal",
        "reason": "No anomaly detected"
    }

    try:
        
        total = float(data.get("total_amount") or 0)
        tax = float(data.get("tax_amount") or 0)
        vendor = str(data.get("vendor_name") or "").lower()

      
        test_df = pd.DataFrame({
            "total_amount": [total],
            "tax": [tax]
        })

        prediction = model.predict(test_df)

        
        if prediction[0] == -1:
            result["status"] = "Suspicious"
            result["reason"] = "Anomalous invoice pattern detected"

      
        if total > 100000:
            result["status"] = "Suspicious"
            result["reason"] = "Unusually high invoice amount"

        if "unknown" in vendor or vendor.strip() == "":
            result["status"] = "Suspicious"
            result["reason"] = "Vendor information missing or invalid"

        return result

    except Exception as e:
        return {
            "status": "Error",
            "reason": str(e)
        }