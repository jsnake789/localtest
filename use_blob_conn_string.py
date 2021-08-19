import os

#Import the client object from the SDK library
from azure.storage.blob import BlobClient

#Get the connection string
conn_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]

#Create the client object using the connection string
blob_client = BlobClient.from_connection_string(conn_string,
    container_name="blob-container-01", blob_name="sample-blob.txt")

#Open a local file and upload its contents to Blob Storage
with open("./sample-source.txt", "rb") as data:
    blob_client.upload_blob(data)