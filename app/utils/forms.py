from datetime import datetime, date

def register_filters(app):
    @app.template_filter("dmy")
    def dmy(v):
        if not v: return ""
        if isinstance(v, (datetime, date)):
            return v.strftime("%d-%m-%Y")
        try:
            return datetime.fromisoformat(str(v)).strftime("%d-%m-%Y")
        except Exception:
            return str(v)