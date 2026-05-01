from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

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