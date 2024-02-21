import os
from azure.storage.blob import BlobServiceClient
from datetime import datetime


def write_to_file():
    file = open(file="src/data/report.txt", mode="w")
    file.write("Hello, World!")
    file.close()


def send_blob_to_azure():
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    today_date = datetime.date(datetime.now())
    filename = "report" + today_date.strftime("%Y%m%d") + ".txt"
    blob_client = blob_service_client.get_blob_client(
        container="blobcontainer", blob=filename
    )
    with open(file="src/data/report.txt", mode="rb") as data:
        blob_client.upload_blob(data)
