from flask import Flask
from app.routes import main

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")
app.secret_key = "supersecretkey"

app.register_blueprint(main)

<<<<<<< HEAD
def detect_fraud(data):

    try:
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

    except:
        return "Fraud detection failed"
    
    
=======
if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> main
