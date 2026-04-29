# Financial Document Analysis System Using AI

A smart AI-based system that automates invoice processing using OCR, NLP, and machine learning techniques. This project extracts, validates, and analyzes financial documents such as invoices and receipts.

---

## 🚀 Features

* Upload invoices (PDF or Image)
* OCR-based text extraction
* Automatic invoice data extraction
* Validation of invoice fields
* Fraud detection using machine learning
* Data storage in CSV
* Clean and interactive UI

---

## 🧠 Technologies Used

* Python
* Flask
* OpenCV (cv2)
* Tesseract OCR
* spaCy (NLP)
* Scikit-learn (ML - Isolation Forest)
* Pandas
* HTML, CSS (Frontend)

---

## ⚙️ System Workflow

Upload Document → OCR → Data Extraction → Validation → Fraud Detection → Store Data → Display Results

---

## 📂 Project Structure

```
Financial-Document-AI/
│
├── app/
│   ├── services/
│   │   ├── ocr_service.py
│   │   ├── extraction_service.py
│   │   ├── validation_service.py
│   │   ├── fraud_service.py
│   │   ├── analytics_service.py
│   │
│   ├── templates/
│   │   ├── index.html
│   │   ├── result.html
│   │
│   ├── routes.py
│
├── app.py
├── config.py
├── requirements.txt
├── invoice_database.csv
```

---

## ▶️ How to Run the Project

1. Clone the repository

```
git clone https://github.com/abhii-creep-hub/Financial_Doc_Analysis.git
```

2. Navigate to project folder

```
cd Financial_Doc_Analysis
```

3. Create virtual environment

```
python -m venv .venv
```

4. Activate environment

```
.\.venv\Scripts\activate
```

5. Install dependencies

```
pip install -r requirements.txt
```

6. Run the application

```
python app.py
```

7. Open in browser

```
http://127.0.0.1:5000
```

---

## 📊 Output

* Extracted invoice details
* Validation status
* Fraud detection result
* OCR extracted text

---

## 🎯 Use Case

This system can be used by:

* Accounting firms
* Finance departments
* Audit systems
* Invoice automation tools

---

## 👨‍💻 Team

* Kartik Budhraja
* Abhinav Kumar Sharma
* Vanshika Sharma

---

## 📌 Future Improvements

* Database integration (SQLite/MySQL)
* Dashboard with analytics charts
* Multi-document batch processing
* Improved fraud detection model
* User authentication system

---

## 📄 License

This project is for educational purposes.
