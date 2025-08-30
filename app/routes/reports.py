from flask import Blueprint, render_template, request
from datetime import datetime, date
from sqlalchemy import func
from ..models import db, DailyLog

reports_bp = Blueprint("reports_bp", __name__)

@reports_bp.route("/monthly")
def monthly():
    f = request.args.get("from")
    t = request.args.get("to")
    if f and t:
        d_from = datetime.fromisoformat(f).date()
        d_to = datetime.fromisoformat(t).date()
    else:
        d_from = date(date.today().year, date.today().month, 1)
        d_to = date.today()
    rows = (db.session.query(DailyLog.status, func.count(DailyLog.id),
                             func.coalesce(func.sum(DailyLog.quantity),0.0),
                             func.coalesce(func.sum(DailyLog.amount),0.0))
            .filter(DailyLog.date>=d_from, DailyLog.date<=d_to)
            .group_by(DailyLog.status).all())
    total_qty = sum(r[2] for r in rows)
    total_amt = sum(r[3] for r in rows)
    return render_template("reports.html", rows=rows, total_qty=total_qty, total_amt=total_amt,
                           d_from=d_from, d_to=d_to)