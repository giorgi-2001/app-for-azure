from typing import IO
from datetime import datetime, timedelta, timezone

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from azure.core.exceptions import HttpResponseError


account_url = "https://learnazurestorage2001.blob.core.windows.net"
container_name = "images"
default_credential = DefaultAzureCredential()

blob_service_client = BlobServiceClient(account_url, credential=default_credential)


def upload_file(content: IO[bytes], filename: str):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    response = blob_client.upload_blob(content, overwrite=True)
    print(response)


def get_file_metadata(filename: str):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    return blob_client.get_blob_properties()


def delete_file(filename: str):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    blob_client.delete_blob()


def list_files():
    container_client = blob_service_client.get_container_client(container_name)
    blobs = container_client.list_blob_names()
    try:
        return list(blobs)
    except HttpResponseError:
        return []


def get_file_by_name(filename: str):
    account_name = "learnazurestorage2001"
    user_delegation_key = blob_service_client.get_user_delegation_key(
        key_start_time=datetime.now(timezone.utc),
        key_expiry_time=datetime.now(timezone.utc) + timedelta(hours=1)
    )
    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=container_name,
        blob_name=filename,
        user_delegation_key=user_delegation_key,
        permission=BlobSasPermissions(read=True, write=False),
        expiry=datetime.now(timezone.utc) + timedelta(hours=1)
    )

    return f"https://{account_name}.blob.core.windows.net/{container_name}/{filename}?{sas_token}"
