#!/usr/bin/env python3
"""
Fix Google Cloud Storage import issues for HF Spaces deployment.
This script patches the storage module to handle missing google-cloud-storage gracefully.
"""

import os
import sys
from pathlib import Path

def patch_storage_init():
    """Patch the storage/__init__.py to handle Google Cloud imports gracefully"""
    
    storage_init_path = Path("openhands/storage/__init__.py")
    
    if not storage_init_path.exists():
        print("❌ Storage __init__.py not found")
        return False
    
    # Read current content
    with open(storage_init_path, 'r') as f:
        content = f.read()
    
    # Check if already patched
    if "GOOGLE_CLOUD_AVAILABLE = False" in content:
        print("✅ Storage module already patched")
        return True
    
    # Create patched content
    patched_content = '''import os

import httpx

from openhands.storage.files import FileStore
from openhands.storage.local import LocalFileStore
from openhands.storage.memory import InMemoryFileStore
from openhands.storage.web_hook import WebHookFileStore

# Conditional imports for optional cloud storage
try:
    from openhands.storage.google_cloud import GoogleCloudFileStore
    GOOGLE_CLOUD_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Google Cloud Storage not available: {e}")
    GOOGLE_CLOUD_AVAILABLE = False
    GoogleCloudFileStore = None

try:
    from openhands.storage.s3 import S3FileStore
    S3_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  S3 Storage not available: {e}")
    S3_AVAILABLE = False
    S3FileStore = None


def get_file_store(
    file_store_type: str,
    file_store_path: str | None = None,
    file_store_web_hook_url: str | None = None,
    file_store_web_hook_headers: dict | None = None,
) -> FileStore:
    store: FileStore
    if file_store_type == 'local':
        if file_store_path is None:
            raise ValueError('file_store_path is required for local file store')
        store = LocalFileStore(file_store_path)
    elif file_store_type == 's3':
        if not S3_AVAILABLE or S3FileStore is None:
            print("⚠️  S3 storage not available, falling back to memory storage")
            store = InMemoryFileStore()
        else:
            store = S3FileStore(file_store_path)
    elif file_store_type == 'google_cloud':
        if not GOOGLE_CLOUD_AVAILABLE or GoogleCloudFileStore is None:
            print("⚠️  Google Cloud storage not available, falling back to memory storage")
            store = InMemoryFileStore()
        else:
            store = GoogleCloudFileStore(file_store_path)
    else:
        store = InMemoryFileStore()
    
    if file_store_web_hook_url:
        if file_store_web_hook_headers is None:
            # Fallback to default headers. Use the session api key if it is defined in the env.
            file_store_web_hook_headers = {}
            if os.getenv('SESSION_API_KEY'):
                file_store_web_hook_headers['X-Session-API-Key'] = os.getenv(
                    'SESSION_API_KEY'
                )
        store = WebHookFileStore(
            store,
            file_store_web_hook_url,
            httpx.Client(headers=file_store_web_hook_headers or {}),
        )
    return store
'''
    
    # Write patched content
    with open(storage_init_path, 'w') as f:
        f.write(patched_content)
    
    print("✅ Storage module patched successfully")
    return True

def patch_google_cloud_storage():
    """Create a dummy google.cloud.storage module if it doesn't exist"""
    
    google_cloud_path = Path("openhands/storage/google_cloud.py")
    
    if not google_cloud_path.exists():
        print("❌ Google Cloud storage module not found")
        return False
    
    # Read current content
    with open(google_cloud_path, 'r') as f:
        content = f.read()
    
    # Check if already patched
    if "# HF Spaces compatibility patch" in content:
        print("✅ Google Cloud storage module already patched")
        return True
    
    # Create patched content with better error handling
    patched_content = '''# HF Spaces compatibility patch
import os

try:
    from google.api_core.exceptions import NotFound
    from google.cloud import storage
    from google.cloud.storage.blob import Blob
    from google.cloud.storage.bucket import Bucket
    from google.cloud.storage.client import Client
    GOOGLE_CLOUD_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Google Cloud dependencies not available: {e}")
    GOOGLE_CLOUD_AVAILABLE = False
    # Create dummy classes
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
'''
    
    # Write patched content
    with open(google_cloud_path, 'w') as f:
        f.write(patched_content)
    
    print("✅ Google Cloud storage module patched successfully")
    return True

def main():
    """Main function to apply all patches"""
    print("🔧 Fixing Google Cloud Storage import issues...")
    
    success = True
    success &= patch_storage_init()
    success &= patch_google_cloud_storage()
    
    if success:
        print("✅ All patches applied successfully!")
        print("💡 Google Cloud Storage will gracefully fallback to memory storage if not available")
    else:
        print("❌ Some patches failed")
        sys.exit(1)

if __name__ == "__main__":
    main()