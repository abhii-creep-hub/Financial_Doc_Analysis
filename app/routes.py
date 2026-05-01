import os
from flask import Blueprint, render_template, request, redirect
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user

from app.models import db, User, Invoice

from app.services.ocr_service import extract_text
from app.services.extraction_service import extract_invoice_data

main = Blueprint('main', __name__)

UPLOAD_FOLDER = "app/uploads"

# ---------------- HOME ----------------
@main.route('/')
@login_required
def home():
    return render_template('index.html')

# ---------------- UPLOAD ----------------
@main.route('/upload', methods=['POST'])
@login_required
def upload_file():
    try:
        if 'invoice_file' not in request.files:
            return "No file uploaded"

        file = request.files['invoice_file']

        if file.filename == '':
            return "Empty file"

        filename = secure_filename(file.filename)
        filepath = os.path.join("app/uploads", filename)

        os.makedirs("app/uploads", exist_ok=True)
        file.save(filepath)

        # OCR
        try:
            text = extract_text(filepath)
        except Exception as e:
            return f"OCR ERROR: {str(e)}"

        # Extraction
        try:
            data = extract_invoice_data(text)
        except Exception as e:
            return f"EXTRACTION ERROR: {str(e)}"

        return render_template("result.html",
                       invoice_data=data,
                       extracted_text=text,
                       validation_result={},
                       fraud_result={})

    except Exception as e:
        return f"MAIN ERROR: {str(e)}"
    
# ---------------- SIGNUP ----------------
@main.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=request.form["password"]
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/login")

    return render_template("signup.html")

# ---------------- LOGIN ----------------
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()

        if user and user.password == request.form["password"]:
            login_user(user)
            return redirect("/")

    return render_template("login.html")

# ---------------- LOGOUT ----------------
@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")