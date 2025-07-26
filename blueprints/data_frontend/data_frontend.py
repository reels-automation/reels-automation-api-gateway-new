import os
import logging
import requests
from datetime import timedelta
from minio_client import get_minio_client_to_sign_signatures
from minio import Minio
from fastapi import APIRouter, HTTPException, status, Depends
from dotenv import load_dotenv

load_dotenv()
ollama_ip = os.getenv("OLLAMA_IP")
data_router = APIRouter()
logger = logging.getLogger(__name__)

@data_router.get("/ollama-models")
async def get_ollama_models():
    try:
        url = f"{ollama_ip}/api/tags"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        models = response.json()['models']

        parsed_models = []
        for model in models:
            parsed_models.append(model["name"])
        print(parsed_models)
        return {"models": parsed_models, "error": None}
    except Exception as e:
        error = f"Error al hacer fetch al endpoint de ollama"
        logger.log(logging.ERROR, error)
        return {"models": [], "error": error}

@data_router.get("/gameplays")
async def get_gameplays(
    minio_client: Minio = Depends(get_minio_client_to_sign_signatures)
):
    bucket_name = "gameplays"
    objects = minio_client.list_objects(bucket_name, recursive=False)
    object_names = [obj.object_name for obj in objects]
    data = []
    for object in object_names:
        url = minio_client.presigned_get_object(
                bucket_name, object, expires=timedelta(days=7))
        
        info = {"name":object, "url": url}
        data.append(info)

    return data
