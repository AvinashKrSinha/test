# app/clients/gcs.py
import logging
from google.cloud import storage
from app.config import settings

logger = logging.getLogger("factcheck_service")

class GCSClient:
    def __init__(self):
        self.client = storage.Client()
        self.bucket = self.client.bucket(settings.gcs_bucket)
    
    def upload_file(self, file_bytes: bytes, destination_path: str):
        blob = self.bucket.blob(destination_path)
        blob.upload_from_string(file_bytes)
        logger.info(f"Uploaded file to GCS: {destination_path}")
        return f"gs://{settings.gcs_bucket}/{destination_path}"

    def download_file(self, path: str) -> bytes:
        blob = self.bucket.blob(path)
        content = blob.download_as_bytes()
        logger.info(f"Downloaded file from GCS: {path}")
        return content
