from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from datetime import date, datetime
from ..models import db, Customer, DailyLog
from ..utils.calculations import calc_amount
from ..utils.exports import to_csv_response, to_excel_response

logs_bp = Blueprint("logs_bp", __name__)

@logs_bp.route("/", methods=["GET","POST"])
def index():
    # Add / Edit handler
    if request.method == "POST":
        transaction_type = request.form.get("transaction_type")
        customer_id = int(request.form["customer_id"])
        dt = datetime.fromisoformat(request.form.get("date") or str(date.today())).date()
        status = request.form.get("status")
        note = request.form.get("note","").strip()
        generate_invoice = request.form.get("generate_invoice") == "yes"
        
        if transaction_type == "milk":
            # Milk transaction
            qty = float(request.form.get("quantity") or 0)
            
            # Handle sample weight input
            sw_input = request.form.get("sample_weight") or "0.220"
            if sw_input.replace('.', '', 1).isdigit():
                sw = float(sw_input)
                if sw > 1:  # If user entered 220 instead of 0.220
                    sw = sw / 1000
            else:
                sw = 0.220
                
            rate = float(request.form.get("rate") or current_app.config["DEFAULT_MILK_RATE"])
            amount = calc_amount(qty, sw, rate)
            withdraw = 0.0
        else:
            # Money transaction
            qty = 0.0
            sw = 0.0
            rate = 0.0
            amount = float(request.form.get("amount") or 0)
            withdraw = 0.0

        item = DailyLog()
        db.session.add(item)

        item.date = dt
        item.customer_id = customer_id
        item.quantity = qty
        item.sample_weight = sw
        item.rate = rate
        item.status = status
        item.amount = amount
        item.withdraw = withdraw
        item.note = note
        db.session.commit()
        
        flash("Log saved", "success")
        
        # Generate invoice if requested
        if generate_invoice:
            return redirect(url_for("logs_bp.invoice", id=item.id))
            
        return redirect(url_for("logs_bp.index", date=str(dt), customer_id=customer_id))

    # GET view with filters
    cur = request.args.get("date")
    customer_id = request.args.get("customer_id")
    try:
        selected = datetime.fromisoformat(cur).date() if cur else date.today()
    except Exception:
        selected = date.today()

    # Get logs for selected date
    logs = DailyLog.query.filter_by(date=selected)
    if customer_id:
        logs = logs.filter_by(customer_id=customer_id)
    logs = logs.order_by(DailyLog.id.desc()).all()
    
    customers = Customer.query.order_by(Customer.name.asc()).all()
    selected_customer = Customer.query.get(customer_id) if customer_id else None

    # Export
    if request.args.get("export") == "csv":
        rows = [[x.date, x.customer.name, x.quantity, x.sample_weight, x.rate, x.amount, x.status, 
                x.amount if (x.status or "").lower() == "credit" and x.quantity == 0 else 0,
                x.amount if (x.status or "").lower() == "debit" else 0,
                x.note] for x in logs]
        return to_csv_response(f"daily_{selected}.csv", rows,
                               ["Date","Customer","Qty","SampleWt","Rate","Amount","Status","Credit","Debit","Note"])
    
    if request.args.get("export") == "xlsx":
        rows = [[x.date, x.customer.name, x.quantity, x.sample_weight, x.rate, x.amount, x.status,
                x.amount if (x.status or "").lower() == "credit" and x.quantity == 0 else 0,
                x.amount if (x.status or "").lower() == "debit" else 0,
                x.note] for x in logs]
        return to_excel_response(f"daily_{selected}.xlsx", rows,
                                 ["Date","Customer","Qty","SampleWt","Rate","Amount","Status","Credit","Debit","Note"])

    return render_template("logs.html", logs=logs, customers=customers, selected=selected, selected_customer=selected_customer)

@logs_bp.post("/delete/<int:id>")
def delete(id):
    x = DailyLog.query.get_or_404(id)
    db.session.delete(x)
    db.session.commit()
    flash("Deleted", "warning")
    return redirect(url_for("logs_bp.index", date=str(x.date)))

@logs_bp.route("/invoice/<int:id>")
def invoice(id):
    log = DailyLog.query.get_or_404(id)
    return render_template("logs/invoice.html", log=log)