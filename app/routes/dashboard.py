from flask import Blueprint, render_template, request, current_app
from datetime import date, datetime, timedelta
from sqlalchemy import func
from ..models import db, Customer, DailyLog
from ..utils.exports import to_csv_response, to_excel_response

dashboard_bp = Blueprint("dashboard_bp", __name__)

@dashboard_bp.route("/")
def dashboard():
    q_from = request.args.get("from")
    q_to = request.args.get("to")
    try:
        d_from = datetime.fromisoformat(q_from).date() if q_from else date.today() - timedelta(days=30)
        d_to = datetime.fromisoformat(q_to).date() if q_to else date.today()
    except Exception:
        d_from = date.today() - timedelta(days=30)
        d_to = date.today()

    # widgets - filter by date range
    total_qty = db.session.query(func.coalesce(func.sum(DailyLog.quantity), 0.0)).filter(
        DailyLog.date >= d_from, DailyLog.date <= d_to
    ).scalar()
    
    total_revenue = db.session.query(func.coalesce(func.sum(DailyLog.amount), 0.0)).filter(
        DailyLog.date >= d_from, DailyLog.date <= d_to
    ).scalar()
    
    total_customers = db.session.query(func.count(Customer.id)).scalar()

    # 7 day trend
    start = date.today() - timedelta(days=6)
    trend = (
        db.session.query(DailyLog.date, func.coalesce(func.sum(DailyLog.quantity), 0.0))
        .filter(DailyLog.date >= start)
        .group_by(DailyLog.date).order_by(DailyLog.date).all()
    )

    # day/range transactions
    logs = (
        DailyLog.query.filter(DailyLog.date >= d_from, DailyLog.date <= d_to)
        .order_by(DailyLog.date.desc(), DailyLog.id.desc()).all()
    )
    
    # Export functionality
    if request.args.get("export") == "csv":
        rows = [[x.date, x.customer.name, x.quantity, x.amount, x.status] for x in logs]
        return to_csv_response(f"dashboard_{d_from}_{d_to}.csv", rows, 
                              ["Date","Customer","Qty","Amount","Status"])
    
    if request.args.get("export") == "xlsx":
        rows = [[x.date, x.customer.name, x.quantity, x.amount, x.status] for x in logs]
        return to_excel_response(f"dashboard_{d_from}_{d_to}.xlsx", rows,
                                ["Date","Customer","Qty","Amount","Status"])

    return render_template("dashboard.html",
                           d_from=d_from, d_to=d_to,
                           total_qty=total_qty, total_revenue=total_revenue,
                           total_customers=total_customers, trend=trend, logs=logs)