from datetime import date, datetime
from . import db

def generate_customer_code(base_date=None, seq=1):
    d = base_date or date.today()
    return f"{d:%Y%m%d}{seq:03d}"

class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    customer_code = db.Column(db.String(16), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True, index=True)
    address = db.Column(db.String(200), nullable=True)
    joining_date = db.Column(db.Date, default=date.today, nullable=False)

    logs = db.relationship("DailyLog", backref="customer", lazy=True, cascade="all, delete-orphan")

class DailyLog(db.Model):
    __tablename__ = "daily_logs"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.today, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)

    quantity = db.Column(db.Float, default=0.0)        # litres
    sample_weight = db.Column(db.Float, default=0.220) # kg per litre sample
    rate = db.Column(db.Float, default=190.0)
    withdraw = db.Column(db.Float, default=0.0)        # money withdrawn by customer
    note = db.Column(db.String(250), default="")
    status = db.Column(db.String(12), default="Credit")  # Paid/Credit/Debit
    amount = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)