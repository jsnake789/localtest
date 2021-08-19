import os
from azure.identity import DefaultAzureCredential

#Don't have proper permissions to grant access and use this

#Import the client object from the SDK library
from azure.storage.blob import BlobClient

credential = DefaultAzureCredential()

#Retrieve the storage blob service URL
storage_url = os.environ["STORAGE_BLOB_URL"]

#Create the client object using the storage URL and the credential
blob_client = BlobClient(storage_url,
    container_name="blob-container-01", blob_name="sample-blob.txt", credential=credential)

#Open a local file and upload its contents to Blob Storage
with open("./sample-source.txt", "rb") as data:
    blob_client.upload_blob(data)