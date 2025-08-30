from datetime import date, datetime
from app import db

class SweetCustomer(db.Model):
    __tablename__ = "sweet_customers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True, index=True)
    address = db.Column(db.String(200), nullable=True)
    joining_date = db.Column(db.Date, default=date.today, nullable=False)

    txns = db.relationship("SweetTransaction", backref="customer", lazy=True, cascade="all, delete-orphan")

class SweetTransaction(db.Model):
    __tablename__ = "sweet_transactions"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.today, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("sweet_customers.id"), nullable=False)
    khoya_type = db.Column(db.String(20), default="Cow_Khoya")  # Cow_Khoya / Buffalo_Khoya
    weight = db.Column(db.Float, default=0.0)
    rate = db.Column(db.Float, default=310.0)
    amount = db.Column(db.Float, default=0.0)
    credit = db.Column(db.Float, default=0.0)
    note = db.Column(db.String(250), default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)