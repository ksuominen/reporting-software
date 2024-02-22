from flask import Flask
from src.queries import db_get_workhours, db_cumulative_hours_by_customers
from src.write_and_store import write_to_file, send_blob_to_azure
from datetime import datetime


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return {"index": True}


@app.route("/report/<date>", methods=["GET"])
def send_report_by_day(date):
    try:
        date_ob = datetime.strptime(date, "%Y%m%d")
    except:
        return {"error": "incorrect date format,  should be YYYYMMDD"}
    try:
        workhours = db_get_workhours(date_ob)
        cumulative_hours = db_cumulative_hours_by_customers(date_ob)
        write_to_file(workhours, cumulative_hours, date_ob)
        send_blob_to_azure(date_ob)
        return {"success": "report sent to Azure"}
    except:
        return {"error": "error with creating report"}
