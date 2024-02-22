import os
from azure.storage.blob import BlobServiceClient
from datetime import datetime


def write_to_file(workhours, cumulative_workhours, date=datetime.now()):
    datestr = datetime.date(date).strftime("%d.%m.%Y")
    file = open(file="data/report.txt", mode="w")
    first_row = f"This is a report for {datestr}\n"
    file.write(first_row)
    for result in workhours:
        consult, customer, date, hours = result
        row = f"{str(date)} consult: {consult}, customer: {customer}, hours: {hours}\n"
        file.write(row)
    file.write("\n")
    file.write("Cumulative hours per customer\n")
    for result in cumulative_workhours:
        consult, customer, cumulative_workhours = result
        row = f"customer: {customer}, cumulative hours: {cumulative_workhours}, consult: {consult}\n"
        file.write(row)
    file.close()


def send_blob_to_azure(date=datetime.now()):
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    date_ob = datetime.date(date)
    filename = "report" + date_ob.strftime("%Y%m%d") + ".txt"
    blob_client = blob_service_client.get_blob_client(
        container="blobcontainer", blob=filename
    )
    with open(file="data/report.txt", mode="rb") as data:
        blob_client.upload_blob(data)
