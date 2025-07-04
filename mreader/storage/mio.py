import os
from dotenv import load_dotenv
from miniopy_async import Minio as AsyncMinio
from minio import Minio
from minio.commonconfig import ENABLED
from minio.versioningconfig import VersioningConfig
from mreader.reader.filetype import FileType

load_dotenv()
ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')
MINIO_HOST = os.environ.get('MINIO_HOST')
MINIO_PORT = os.environ.get('MINIO_PORT')


def setup_storage():
    storage = Minio(endpoint=f"{MINIO_HOST}:{MINIO_PORT}", access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)
    for tp in FileType:
        bucket_name = str(tp)
        found = storage.bucket_exists(bucket_name)
        if not found:
            storage.make_bucket(bucket_name)
        storage.set_bucket_versioning(bucket_name, VersioningConfig(ENABLED))


def get_storage():
    if ACCESS_KEY is None or SECRET_KEY is None or MINIO_HOST is None or MINIO_PORT is None:
        return None
    setup_storage()
    mio = AsyncMinio(endpoint=f"{MINIO_HOST}:{MINIO_PORT}", access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)
    return mio


def get_sync_storage():
    if ACCESS_KEY is None or SECRET_KEY is None or MINIO_HOST is None or MINIO_PORT is None:
        return None
    mio = Minio(endpoint=f"{MINIO_HOST}:{MINIO_PORT}", access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)
    return mio
