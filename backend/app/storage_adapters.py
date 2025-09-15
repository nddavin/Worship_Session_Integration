from dotenv import load_dotenv
import os
from celery import Celery
from typing import Any, Dict
from datetime import datetime, timedelta, timezone
import boto3
from botocore.exceptions import NoCredentialsError
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

# Load environment variables from .env file
load_dotenv()

# Configure the Celery app using environment variables
app = Celery(
    __name__,
    broker=os.getenv('CELERY_BROKER_URL', 'pyamqp://guest@localhost//'),
    backend=os.getenv('CELERY_RESULT_BACKEND', 'rpc://')
)

# Define your tasks
@app.task
def example_task(param: Any) -> str:
    # Your task implementation here
    return f"Task executed with param: {param}"

@app.task
def another_task(param1: Any, param2: Any) -> str:
    # Your task implementation here
    return f"Another task executed with params: {param1}, {param2}"

# AWS S3 Storage Adapter
def get_s3_client() -> boto3.client:
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_REGION')
    
    if not aws_access_key_id or not aws_secret_access_key or not aws_region:
        raise ValueError("AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION must be provided")
    
    return boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

def upload_to_s3(fileobj: Any, bucket: str, object_name: str) -> Dict[str, Any]:
    s3_client = get_s3_client()
    if not bucket or not object_name:
        return {"error": "Bucket and object_name must be provided"}
    
    try:
        s3_client.upload_fileobj(fileobj, bucket, object_name)
        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucket, 'Key': object_name},
            ExpiresIn=3600
        )
        return {
            "url": url,
            "bucket": bucket,
            "object_name": object_name
        }
    except NoCredentialsError:
        return {"error": "Credentials not available"}
    except Exception as e:
        return {"error": str(e)}

# Google Cloud Storage Adapter
def get_gcs_client() -> Any:
    from google.cloud import storage
    return storage.Client()

def upload_to_gcs(fileobj: Any, bucket_name: str, object_name: str) -> Dict[str, Any]:
    gcs_client = get_gcs_client()
    if not bucket_name or not object_name:
        return {"error": "Bucket name and object_name must be provided"}
    
    bucket = gcs_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    try:
        blob.upload_from_file(fileobj)
        url = blob.generate_signed_url(
            version='v4',
            expiration=timedelta(hours=1),
            method='GET'
        )
        return {
            "url": url,
            "bucket": bucket_name,
            "object_name": object_name
        }
    except Exception as e:
        return {"error": str(e)}

# Azure Storage Adapter
def get_azure_blob_service_client() -> BlobServiceClient:
    account_name = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
    account_key = os.getenv('AZURE_STORAGE_ACCOUNT_KEY')
    if not account_name or not account_key:
        raise ValueError("AZURE_STORAGE_ACCOUNT_NAME and AZURE_STORAGE_ACCOUNT_KEY must be provided")
    
    return BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)

def upload_to_azure(fileobj: Any, container_name: str, blob_name: str) -> Dict[str, Any]:
    blob_service_client = get_azure_blob_service_client()
    if not container_name or not blob_name:
        return {"error": "Container name and blob name must be provided"}
    
    container_client = blob_service_client.get_container_client(container_name)
    try:
        container_client.upload_blob(blob_name, fileobj)
        sas = generate_blob_sas(
            account_name=os.getenv('AZURE_STORAGE_ACCOUNT_NAME'),
            container_name=container_name,
            blob_name=blob_name,
            account_key=os.getenv('AZURE_STORAGE_ACCOUNT_KEY'),
            permission=BlobSasPermissions(read=True),
            expiry=datetime.now(timezone.utc) + timedelta(hours=1)
        )
        url = f"https://{os.getenv('AZURE_STORAGE_ACCOUNT_NAME')}.blob.core.windows.net/{container_name}/{blob_name}?{sas}"
        return {
            "url": url,
            "container": container_name,
            "blob_name": blob_name
        }
    except Exception as e:
        return {"error": str(e)}
