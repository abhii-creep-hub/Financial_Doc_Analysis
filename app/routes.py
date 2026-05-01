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

    file = request.files['invoice_file']

    if file.filename == '':
        return "No file"
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    text = extract_text(filepath)
    data = extract_invoice_data(text)

    # SAVE TO DB
    invoice = Invoice(
        filename=filename,
        user_id=current_user.id,
        invoice_number=data["invoice_number"],
        vendor_name=data["vendor_name"],
        invoice_date=data["invoice_date"],
        total_amount=data["total_amount"],
        tax_amount=data["tax_amount"]
    )

    db.session.add(invoice)
    db.session.commit()

    return render_template("result.html", invoice_data=data, extracted_text=text)

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