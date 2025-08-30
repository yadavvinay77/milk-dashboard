from flask import render_template, request, redirect, url_for, flash, jsonify
from . import sweet_export_bp
from .models import SweetCustomer, SweetTransaction
from app import db
from datetime import date, datetime
from sqlalchemy import func

@sweet_export_bp.route("/")
def index():
    customer_id = request.args.get("customer_id")
    d_from = request.args.get("from")
    d_to = request.args.get("to")
    filter_type = request.args.get("type")
    
    customers = SweetCustomer.query.order_by(SweetCustomer.name.asc()).all()
    
    # Get transactions
    query = SweetTransaction.query
    if customer_id:
        query = query.filter_by(customer_id=customer_id)
    if d_from:
        query = query.filter(SweetTransaction.date >= datetime.fromisoformat(d_from).date())
    if d_to:
        query = query.filter(SweetTransaction.date <= datetime.fromisoformat(d_to).date())
    if filter_type:
        if filter_type == 'credit':
            query = query.filter(SweetTransaction.credit > 0)
        else:
            query = query.filter_by(khoya_type=filter_type)
    
    logs = query.order_by(SweetTransaction.date.desc()).all()
    
    selected_customer = SweetCustomer.query.get(customer_id) if customer_id else None
    
    return render_template(
        "sweet_export/index.html",
        logs=logs,
        customers=customers,
        selected_customer=selected_customer,
        d_from=d_from,
        d_to=d_to,
        today=date.today().isoformat()
    )

@sweet_export_bp.route("/add_customer", methods=["POST"])
def add_customer():
    name = request.form.get("name")
    phone = request.form.get("phone")
    address = request.form.get("address")
    
    if not name:
        flash("Customer name is required", "danger")
        return redirect(url_for("sweet_export_bp.index"))
    
    customer = SweetCustomer(name=name, phone=phone, address=address)
    db.session.add(customer)
    db.session.commit()
    
    flash("Customer added successfully", "success")
    return redirect(url_for("sweet_export_bp.index", customer_id=customer.id))

@sweet_export_bp.route("/add_transaction", methods=["POST"])
def add_transaction():
    customer_id = request.form.get("customer_id")
    khoya_type = request.form.get("khoya_type")
    weight = float(request.form.get("weight", 0))
    rate = float(request.form.get("rate", 0))
    note = request.form.get("note", "")
    transaction_date = request.form.get("date")
    
    if not customer_id:
        flash("Customer is required", "danger")
        return redirect(url_for("sweet_export_bp.index"))
    
    if not transaction_date:
        transaction_date = date.today()
    else:
        transaction_date = datetime.fromisoformat(transaction_date).date()
    
    amount = weight * rate
    
    transaction = SweetTransaction(
        customer_id=customer_id,
        date=transaction_date,
        khoya_type=khoya_type,
        weight=weight,
        rate=rate,
        amount=amount,
        credit=0,
        note=note
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    flash("Transaction added successfully", "success")
    
    if request.form.get("generate_invoice") == "yes":
        return redirect(url_for("sweet_export_bp.invoice", id=transaction.id))
    
    return redirect(url_for("sweet_export_bp.index", customer_id=customer_id))

@sweet_export_bp.route("/add_credit", methods=["POST"])
def add_credit():
    customer_id = request.form.get("customer_id")
    credit_amount = float(request.form.get("credit", 0))
    note = request.form.get("note", "")
    transaction_date = request.form.get("date")
    
    if not customer_id:
        flash("Customer is required", "danger")
        return redirect(url_for("sweet_export_bp.index"))
    
    if not transaction_date:
        transaction_date = date.today()
    else:
        transaction_date = datetime.fromisoformat(transaction_date).date()
    
    transaction = SweetTransaction(
        customer_id=customer_id,
        date=transaction_date,
        khoya_type="Credit",
        weight=0,
        rate=0,
        amount=0,
        credit=credit_amount,
        note=note
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    flash("Credit transaction added successfully", "success")
    
    if request.form.get("generate_invoice") == "yes":
        return redirect(url_for("sweet_export_bp.invoice", id=transaction.id))
    
    return redirect(url_for("sweet_export_bp.index", customer_id=customer_id))

@sweet_export_bp.route("/edit_transaction/<int:id>", methods=["GET", "POST"])
def edit_transaction(id):
    transaction = SweetTransaction.query.get_or_404(id)
    
    if request.method == "POST":
        transaction.date = datetime.fromisoformat(request.form.get("date")).date()
        transaction.khoya_type = request.form.get("khoya_type")
        transaction.weight = float(request.form.get("weight", 0))
        transaction.rate = float(request.form.get("rate", 0))
        transaction.note = request.form.get("note", "")
        
        if transaction.khoya_type == "Credit":
            transaction.credit = float(request.form.get("credit", 0))
            transaction.amount = 0
        else:
            transaction.amount = transaction.weight * transaction.rate
            transaction.credit = 0
        
        db.session.commit()
        flash("Transaction updated successfully", "success")
        return redirect(url_for("sweet_export_bp.index", customer_id=transaction.customer_id))
    
    return render_template("sweet_export/edit.html", transaction=transaction)

@sweet_export_bp.route("/delete_customer/<int:id>", methods=["POST"])
def delete_customer(id):
    customer = SweetCustomer.query.get_or_404(id)
    
    # Delete all related transactions
    SweetTransaction.query.filter_by(customer_id=id).delete()
    
    db.session.delete(customer)
    db.session.commit()
    
    flash("Customer and all related transactions deleted", "warning")
    return redirect(url_for("sweet_export_bp.index"))

@sweet_export_bp.route("/delete_transaction/<int:id>", methods=["POST"])
def delete_transaction(id):
    transaction = SweetTransaction.query.get_or_404(id)
    customer_id = transaction.customer_id
    db.session.delete(transaction)
    db.session.commit()
    
    flash("Transaction deleted", "warning")
    return redirect(url_for("sweet_export_bp.index", customer_id=customer_id))

@sweet_export_bp.route("/invoice/<int:id>")
def invoice(id):
    transaction = SweetTransaction.query.get_or_404(id)
    return render_template("sweet_export/invoice.html", tx=transaction)