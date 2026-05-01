import os
from flask import Flask
from app.routes import main

# NEW IMPORTS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)

# Secret key
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

# Production config
app.config["ENV"] = os.environ.get("FLASK_ENV", "production")
app.config["DEBUG"] = False

# ---------------- DATABASE ----------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------------- LOGIN ----------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "main.login"

# ---------------- MODELS ----------------
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    invoice_number = db.Column(db.String(100))
    vendor_name = db.Column(db.String(200))
    invoice_date = db.Column(db.String(100))
    total_amount = db.Column(db.Float)
    tax_amount = db.Column(db.Float)

# ---------------- LOAD USER ----------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------- INIT DB ----------------
with app.app_context():
    db.create_all()

# ---------------- UPLOAD FOLDER ----------------
UPLOAD_FOLDER = os.path.join("app", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- ROUTES ----------------
app.register_blueprint(main)

# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)