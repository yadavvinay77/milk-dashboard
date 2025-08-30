import csv, io
from flask import Response
import pandas as pd

def to_csv_response(filename, rows, headers):
    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow(headers)
    writer.writerows(rows)
    return Response(si.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": f"attachment; filename={filename}"})

def to_excel_response(filename, rows, headers):
    df = pd.DataFrame(rows, columns=headers)
    bio = io.BytesIO()
    with pd.ExcelWriter(bio, engine="xlsxwriter") as xw:
        df.to_excel(xw, index=False, sheet_name="Data")
    bio.seek(0)
    return Response(bio.read(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    headers={"Content-Disposition": f"attachment; filename={filename}"})