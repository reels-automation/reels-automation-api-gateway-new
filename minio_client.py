import os
from minio import Minio
from dotenv import load_dotenv

load_dotenv()

minio_access_key = os.getenv("MINIO_ACCESS_KEY")
minio_secret_key = os.getenv("MINIO_SECRET_KEY")
minio_url = os.getenv("MINIO_URL")


def get_minio_client() -> Minio:
    client = Minio(
        minio_url,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
        secure=False,
    )
    return client
