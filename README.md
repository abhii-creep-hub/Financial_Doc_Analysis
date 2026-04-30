# 🚀 Financial Document Analysis System Using AI

An AI-powered system that automates invoice processing using **OCR, NLP, and Machine Learning**.
It extracts, validates, detects fraud, and visualizes financial data through an interactive dashboard.

---

## 🌐 Live Demo

👉 *(Add your Render link here after deployment)*
`https://your-app-name.onrender.com`

---

## ✨ Key Features

* 📄 Upload invoices (PDF / Images)
* 🔍 OCR-based text extraction (Tesseract)
* 🧠 Intelligent data extraction using NLP (spaCy)
* ✅ Invoice validation logic
* 🚨 Fraud detection using ML (Isolation Forest)
* 📊 Analytics dashboard with charts
* 💾 Automatic data storage (CSV)
* 🎨 Modern responsive UI

---

## 🧠 Tech Stack

| Category | Technology                      |
| -------- | ------------------------------- |
| Backend  | Python, Flask                   |
| OCR      | Tesseract, OpenCV               |
| NLP      | spaCy                           |
| ML       | Scikit-learn (Isolation Forest) |
| Data     | Pandas                          |
| Frontend | HTML, CSS, Chart.js             |

---

## ⚙️ System Workflow

```
Upload Invoice → OCR → Data Extraction → Validation → Fraud Detection → Store Data → Dashboard Analytics
```

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
│   │   ├── dashboard.html
│   │
│   ├── static/
│   ├── uploads/
│   ├── routes.py
│
├── app.py
├── config.py
├── requirements.txt
├── invoice_database.csv
└── README.md
```

---

## ▶️ How to Run Locally

### 1. Clone Repository

```
git clone https://github.com/abhii-creep-hub/Financial_Doc_Analysis.git
cd Financial_Doc_Analysis
```

### 2. Create Virtual Environment

```
python -m venv .venv
```

### 3. Activate Environment

```
.\.venv\Scripts\activate
```

### 4. Install Dependencies

```
pip install -r requirements.txt
```

### 5. Run Application

```
python app.py
```

### 6. Open Browser

```
http://127.0.0.1:5000
```

---

## 📊 Output

* Extracted invoice fields (vendor, amount, tax, etc.)
* Validation results
* Fraud detection status
* OCR extracted raw text
* Dashboard analytics (total invoices, revenue, vendor distribution)

---

## 🎯 Use Cases

* 📊 Finance & Accounting automation
* 🧾 Invoice processing systems
* 🏢 Enterprise expense management
* 🔍 Audit & compliance systems

---

## 🚀 Future Improvements

* Database integration (MySQL / PostgreSQL)
* User authentication system
* Batch invoice processing
* Advanced fraud detection models (Deep Learning)
* Cloud deployment optimization
* API-based integration

---

## 👨‍💻 Team

* Kartik Budhraja
* Abhinav Kumar Sharma
* Vanshika Sharma

---

## 📌 Highlights

* End-to-end AI pipeline (OCR → NLP → ML)
* Real-time dashboard analytics
* Modular and scalable architecture
* Deployment-ready Flask application

---

## 📄 License

This project is developed for educational purposes.
