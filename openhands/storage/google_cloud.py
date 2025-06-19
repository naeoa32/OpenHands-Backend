# HF Spaces compatibility patch
# Google Cloud is COMPLETELY OPTIONAL - no login required, no API key needed!
# This file only provides Google Cloud storage option if user wants it
import os

try:
    from google.api_core.exceptions import NotFound
    from google.cloud import storage
    from google.cloud.storage.blob import Blob
    from google.cloud.storage.bucket import Bucket
    from google.cloud.storage.client import Client
    GOOGLE_CLOUD_AVAILABLE = True
except ImportError as e:
    print(f"✅ Google Cloud dependencies not available (PERFECTLY FINE): {e}")
    print("📝 No Google login/API key required - using memory storage instead")
    GOOGLE_CLOUD_AVAILABLE = False
    # Create dummy classes for compatibility
    class NotFound(Exception):
        pass
    class Blob:
        pass
    class Bucket:
        pass
    class Client:
        pass

from openhands.storage.files import FileStore


class GoogleCloudFileStore(FileStore):
    def __init__(self, bucket_name: str | None = None) -> None:
        """Create a new FileStore.

        If GOOGLE_APPLICATION_CREDENTIALS is defined in the environment it will be used
        for authentication. Otherwise access will be anonymous.
        """
        if not GOOGLE_CLOUD_AVAILABLE:
            raise ImportError("Google Cloud Storage not available. Please install google-cloud-storage.")
            
        if bucket_name is None:
            bucket_name = os.environ['GOOGLE_CLOUD_BUCKET_NAME']
        self.bucket_name = bucket_name
        self.client = Client()
        self.bucket = self.client.bucket(bucket_name)

    def read(self, path: str) -> str:
        if not GOOGLE_CLOUD_AVAILABLE:
            raise ImportError("Google Cloud Storage not available")
        blob = self.bucket.blob(path)
        try:
            return blob.download_as_text()
        except NotFound:
            raise FileNotFoundError(f'File not found: {path}')

    def write(self, path: str, contents: str) -> None:
        if not GOOGLE_CLOUD_AVAILABLE:
            raise ImportError("Google Cloud Storage not available")
        blob = self.bucket.blob(path)
        blob.upload_from_string(contents)

    def delete(self, path: str) -> None:
        if not GOOGLE_CLOUD_AVAILABLE:
            raise ImportError("Google Cloud Storage not available")
        blob = self.bucket.blob(path)
        try:
            blob.delete()
        except NotFound:
            raise FileNotFoundError(f'File not found: {path}')

    def exists(self, path: str) -> bool:
        if not GOOGLE_CLOUD_AVAILABLE:
            return False
        blob = self.bucket.blob(path)
        return blob.exists()

    def list(self, path: str) -> list[str]:
        if not GOOGLE_CLOUD_AVAILABLE:
            return []
        blobs = self.client.list_blobs(self.bucket, prefix=path)
        return [blob.name for blob in blobs]
