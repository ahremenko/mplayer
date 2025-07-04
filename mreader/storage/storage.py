import logging

logger = logging.getLogger(__name__)


async def save_file_to_s3(storage, bucket_name, file_path):
    result = await storage.fput_object(bucket_name, file_path, file_path)
    return str({"bucket_name": bucket_name, "object_name": result.object_name, "version_id": result.version_id})

