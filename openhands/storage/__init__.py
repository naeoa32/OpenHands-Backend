import os

import httpx

from openhands.storage.files import FileStore
from openhands.storage.local import LocalFileStore
from openhands.storage.memory import InMemoryFileStore
from openhands.storage.web_hook import WebHookFileStore

# Conditional imports for optional cloud storage
try:
    from openhands.storage.google_cloud import GoogleCloudFileStore
    GOOGLE_CLOUD_AVAILABLE = True
except ImportError:
    GOOGLE_CLOUD_AVAILABLE = False
    GoogleCloudFileStore = None

try:
    from openhands.storage.s3 import S3FileStore
    S3_AVAILABLE = True
except ImportError:
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
            raise ImportError('S3 storage not available. Install boto3 to use S3 storage.')
        store = S3FileStore(file_store_path)
    elif file_store_type == 'google_cloud':
        if not GOOGLE_CLOUD_AVAILABLE or GoogleCloudFileStore is None:
            raise ImportError('Google Cloud storage not available. Install google-cloud-storage to use Google Cloud storage.')
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
