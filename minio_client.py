import os
from minio import Minio
from dotenv import load_dotenv

load_dotenv()

# Variables requeridas
required_env_vars = [
    "MINIO_ACCESS_KEY",
    "MINIO_SECRET_KEY",
    "MINIO_URL",
    "MINIO_PUBLIC_URL_SIGN_FILES",
    "SECURE",
]

# Validación de variables de entorno
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    print(f"❌ Faltan variables de entorno: {', '.join(missing_vars)}")
    raise EnvironmentError("Config incompleta, revisa tu archivo .env")

# Si todas están presentes
minio_access_key = os.getenv("MINIO_ACCESS_KEY")
minio_secret_key = os.getenv("MINIO_SECRET_KEY")
minio_url = os.getenv("MINIO_URL")
minio_public_url = os.getenv("MINIO_PUBLIC_URL_SIGN_FILES")

# Convierte SECURE a bool (True si es "true", "1", etc.)
secure = os.getenv("SECURE", "false").lower() in ("true", "1", "yes")


def get_minio_client() -> Minio:
    return Minio(
        minio_url,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
        secure=secure,
    )


def get_minio_client_to_sign_signatures() -> Minio:
    return Minio(
        minio_public_url,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
        secure=secure,
    )
