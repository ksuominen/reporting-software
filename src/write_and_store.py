import os
from azure.storage.blob import BlobServiceClient
from datetime import datetime


def write_to_file(sql_result):
    file = open(file="data/report.txt", mode="w")

    for result in sql_result:
        consult, customer, date, hours = result
        row = f"{str(date)} consult: {consult}, customer: {customer}, hours: {hours}\n"
        file.write(row)
    file.close()


def send_blob_to_azure():
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    today_date = datetime.date(datetime.now())
    filename = "report" + today_date.strftime("%Y%m%d") + ".txt"
    blob_client = blob_service_client.get_blob_client(
        container="blobcontainer", blob=filename
    )
    with open(file="data/report.txt", mode="rb") as data:
        blob_client.upload_blob(data)


from queries import db_get_workhours

if __name__ == ("__main__"):
    sql_result = db_get_workhours("Minja")
    write_to_file(sql_result)
    send_blob_to_azure()
