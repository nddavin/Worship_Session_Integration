# backend/app/storage_adapters.py
import os
from typing import Dict, Tuple
from datetime import datetime, timedelta

ADAPTER = os.getenv("STORAGE_ADAPTER", "s3").lower()

# ---- S3 Adapter ----
class S3Adapter:
    def __init__(self, bucket: str, region: str = None):
        import boto3
        self.bucket = bucket
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=region or os.getenv("AWS_REGION"),
        )

    def generate_upload_url(self, key: str, content_type: str, expires: int = 3600) -> Dict:
        url = self.s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={"Bucket": self.bucket, "Key": key, "ContentType": content_type},
            ExpiresIn=expires,
        )
        return {"url": url, "method": "PUT", "headers": {"Content-Type": content_type}}

    def generate_download_url(self, key: str, expires: int = 3600) -> str:
        return self.s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self.bucket, "Key": key},
            ExpiresIn=expires,
        )

    def upload_fileobj(self, fileobj, key: str, content_type: str = None):
        # server-side fallback using boto3 upload_fileobj
        extra = {"ContentType": content_type} if content_type else {}
        self.s3.upload_fileobj(Fileobj=fileobj, Bucket=self.bucket, Key=key, ExtraArgs=extra)

# ---- GCS Adapter ----
class GCSAdapter:
    def __init__(self, bucket: str):
        from google.cloud import storage as gcs_storage
        self.client = gcs_storage.Client()
        self.bucket = self.client.bucket(bucket)

    def generate_upload_url(self, key: str, content_type: str, expires: int = 3600) -> Dict:
        blob = self.bucket.blob(key)
        url = blob.generate_signed_url(
            expiration=timedelta(seconds=expires),
            method="PUT",
            content_type=content_type,
        )
        return {"url": url, "method": "PUT", "headers": {"Content-Type": content_type}}

    def generate_download_url(self, key: str, expires: int = 3600) -> str:
        blob = self.bucket.blob(key)
        return blob.generate_signed_url(expiration=timedelta(seconds=expires), method="GET")

    def upload_fileobj(self, fileobj, key: str, content_type: str = None):
        blob = self.bucket.blob(key)
        blob.upload_from_file(fileobj, content_type=content_type)

# ---- Azure Adapter ----
class AzureAdapter:
    def __init__(self, account_name: str, container: str, account_key: str = None):
        from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
        self.account_name = account_name
        self.container = container
        self.account_key = account_key or os.getenv("AZURE_ACCOUNT_KEY")
        conn_str = os.getenv("AZURE_CONN_STR")
        if conn_str:
            self.client = BlobServiceClient.from_connection_string(conn_str)
        else:
            self.client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=self.account_key)

    def generate_upload_url(self, key: str, content_type: str, expires: int = 3600) -> Dict:
        from azure.storage.blob import generate_blob_sas, BlobSasPermissions
        expiry = datetime.utcnow() + timedelta(seconds=expires)
        sas = generate_blob_sas(
            account_name=self.account_name,
            container_name=self.container,
            blob_name=key,
            account_key=self.account_key,
            permission=BlobSasPermissions(write=True),
            expiry=expiry,
        )
        url = f"https://{self.account_name}.blob.core.windows.net/{self.container}/{key}?{sas}"
        return {"url": url, "method": "PUT", "headers": {"x-ms-blob-type": "BlockBlob", "Content-Type": content_type}}

    def generate_download_url(self, key: str, expires: int = 3600) -> str:
        from azure.storage.blob import generate_blob_sas, BlobSasPermissions
        expiry = datetime.utcnow() + timedelta(seconds=expires)
        sas = generate_blob_sas(account_name=self.account_name, container_name=self.container, blob_name=key, account_key=self.account_key, permission=BlobSasPermissions(read=True), expiry=expiry)
        return f"https://{self.account_name}.blob.core.windows.net/{self.container}/{key}?{sas}"

    def upload_fileobj(self, fileobj, key: str, content_type: str = None):
        container_client = self.client.get_container_client(self.container)
        container_client.upload_blob(name=key, data=fileobj, overwrite=True, content_settings={"content_type": content_type} if content_type else None)

# ---- Factory ----
def get_adapter():
    adapter_type = ADAPTER
    if adapter_type == "s3":
        return S3Adapter(bucket=os.getenv("S3_BUCKET"), region=os.getenv("AWS_REGION"))
    if adapter_type == "gcs":
        return GCSAdapter(bucket=os.getenv("GCS_BUCKET"))
    if adapter_type == "azure":
        return AzureAdapter(account_name=os.getenv("AZURE_ACCOUNT_NAME"), container=os.getenv("AZURE_CONTAINER"), account_key=os.getenv("AZURE_ACCOUNT_KEY"))
    raise RuntimeError("Unknown STORAGE_ADAPTER set: " + adapter_type)
