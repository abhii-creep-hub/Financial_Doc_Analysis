# Financial Document Analysis System

A college project for automated invoice processing using AI/ML.

**Team: 1709**
- Kartik Budhraja
- Abhinav Kumar Sharma
- Vanshika Sharma

## Project Features

- 📄 Upload invoices (PDF/Images)
- 🤖 Automatic OCR text extraction
- 🔍 NLP-based information extraction
- ✅ Validation against invoice rules
- 📊 Analytics & reporting dashboard
- ⚠️ Overdue invoice detection
- 💾 SQLAlchemy database integration

## Core Pipeline

```
Document Upload → OCR → NLP Extraction → Validation → Analytics → Dashboard
```

## Project Structure

```
financial_doc_analysis_system/
├── app/
│   ├── routes/              # Flask blueprints (endpoints)
│   ├── models/              # Database models
│   ├── services/            # Business logic (OCR, NLP, validation)
│   ├── utils/               # Helper functions
│   ├── templates/           # HTML templates
│   ├── static/              # CSS, JS, images
│   └── __init__.py          # App factory
├── uploads/                 # Uploaded files directory
├── logs/                    # Application logs
├── config.py                # Configuration settings
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Setup Instructions

### 1. Clone/Download Project
```bash
cd financial_doc_analysis_system
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Tesseract OCR
- **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
- **Linux**: `sudo apt-get install tesseract-ocr`
- **Mac**: `brew install tesseract`

### 5. Create Database
Update `config.py` with your MySQL credentials, then:
```bash
# Create database
# MySQL: CREATE DATABASE financial_docs_dev;

# Run migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Run Application
```bash
python run.py
```

Visit: `http://localhost:5000`

## Technology Stack

- **Backend**: Flask, SQLAlchemy
- **OCR**: Tesseract, EasyOCR
- **NLP**: spaCy, Transformers
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Analytics**: Pandas, Plotly, Matplotlib

## Development Guidelines

- Write modular, small functions
- Use meaningful variable names
- Add natural, developer-style comments
- Follow PEP 8 style guide
- Test features before committing

## Next Steps

1. Create database models for invoices
2. Implement document upload API
3. Build OCR service
4. Create NLP extraction logic
5. Add validation rules
6. Build dashboard UI

---

*Last Updated: March 2025*
