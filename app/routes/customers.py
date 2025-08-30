from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date, datetime
from sqlalchemy import or_
from ..models import db, Customer, DailyLog, generate_customer_code
from ..utils.calculations import milk_balance
from ..utils.exports import to_csv_response, to_excel_response

customers_bp = Blueprint("customers_bp", __name__)

@customers_bp.get("/")
def home_redirect():
    return redirect(url_for("customers_bp.list_customers"))

@customers_bp.route("/list")
def list_customers():
    q = request.args.get("q", "")
    join_from = request.args.get("from")
    join_to = request.args.get("to")
    query = Customer.query
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Customer.name.ilike(like),
                                 Customer.phone.ilike(like),
                                 Customer.address.ilike(like),
                                 Customer.customer_code.ilike(like)))
    if join_from:
        query = query.filter(Customer.joining_date >= datetime.fromisoformat(join_from))
    if join_to:
        query = query.filter(Customer.joining_date <= datetime.fromisoformat(join_to))
    rows = query.order_by(Customer.name.asc()).all()
    if request.args.get("export") == "csv":
        data = [[r.customer_code, r.name, r.phone, r.address, r.joining_date] for r in rows]
        return to_csv_response("customers.csv", data, ["Code","Name","Phone","Address","Joined"])
    if request.args.get("export") == "xlsx":
        data = [[r.customer_code, r.name, r.phone, r.address, r.joining_date] for r in rows]
        return to_excel_response("customers.xlsx", data, ["Code","Name","Phone","Address","Joined"])
    return render_template("customers/list.html", rows=rows)

@customers_bp.route("/add", methods=["GET","POST"])
def add_customer():
    if request.method == "POST":
        name = request.form["name"].strip()
        phone = request.form.get("phone","").strip()
        address = request.form.get("address","").strip()
        # generate unique code
        seq = (Customer.query.count() or 0) + 1
        code = generate_customer_code(seq=seq)
        c = Customer(customer_code=code, name=name, phone=phone, address=address)
        db.session.add(c)
        db.session.commit()
        flash("Customer added", "success")
        return redirect(url_for("customers_bp.list_customers"))
    return render_template("customers/add.html")

@customers_bp.route("/<int:id>/edit", methods=["GET","POST"])
def edit_customer(id):
    c = Customer.query.get_or_404(id)
    if request.method == "POST":
        c.name = request.form["name"].strip()
        c.phone = request.form.get("phone","").strip()
        c.address = request.form.get("address","").strip()
        db.session.commit()
        flash("Customer updated", "success")
        return redirect(url_for("customers_bp.list_customers"))
    return render_template("customers/edit.html", c=c)

@customers_bp.route("/<int:id>/delete", methods=["POST"])
def delete_customer(id):
    c = Customer.query.get_or_404(id)
    
    # Delete all related logs first
    DailyLog.query.filter_by(customer_id=id).delete()
    
    db.session.delete(c)
    db.session.commit()
    flash("Customer and all related transactions deleted", "warning")
    return redirect(url_for("customers_bp.list_customers"))

@customers_bp.route("/<int:id>/history")
def history(id):
    c = Customer.query.get_or_404(id)
    f = request.args.get("from")
    t = request.args.get("to")
    q = c.logs
    if f:
        q = [x for x in q if x.date >= datetime.fromisoformat(f).date()]
    if t:
        q = [x for x in q if x.date <= datetime.fromisoformat(t).date()]
    
    total_qty = sum(x.quantity for x in q)
    total_amount = sum(x.amount for x in q)
    
    # Calculate credit and debit totals
    credit_total = sum(x.amount for x in q if (x.status or "").lower() == "credit")
    debit_total = sum(x.amount for x in q if (x.status or "").lower() == "debit")
    balance = credit_total - debit_total
    
    if request.args.get("export") == "csv":
        rows = [[x.date, x.quantity, x.sample_weight, x.rate, x.amount, x.status, 
                x.amount if (x.status or "").lower() == "credit" else 0,
                x.amount if (x.status or "").lower() == "debit" else 0,
                x.note] for x in q]
        return to_csv_response(f"{c.name}_milk_history.csv", rows,
                               ["Date","Qty","SampleWt","Rate","Amount","Status","Credit","Debit","Note"])
    
    if request.args.get("export") == "xlsx":
        rows = [[x.date, x.quantity, x.sample_weight, x.rate, x.amount, x.status,
                x.amount if (x.status or "").lower() == "credit" else 0,
                x.amount if (x.status or "").lower() == "debit" else 0,
                x.note] for x in q]
        return to_excel_response(f"{c.name}_milk_history.xlsx", rows,
                                 ["Date","Qty","SampleWt","Rate","Amount","Status","Credit","Debit","Note"])
    
    return render_template("customers/history.html", c=c, logs=q,
                           total_qty=total_qty, total_amount=total_amount,
                           credit_total=credit_total, debit_total=debit_total, balance=balance)