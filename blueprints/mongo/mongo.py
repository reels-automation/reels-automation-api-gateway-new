# login.py

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from datetime import timedelta
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from database_mongo import get_db
from minio_client import get_minio_client_to_sign_signatures
from minio import Minio

mongo_router = APIRouter()

class ImageItem(BaseModel):
    image_name: str
    image_modifier: str
    file_getter: str
    image_directory: str
    timestamp: int
    duration: int

class AudioItem(BaseModel):
    tts_audio_name: str
    tts_audio_directory: str
    file_getter: str
    pitch: int
    tts_voice: str
    tts_rate: int
    pth_voice: str

class SubtitleItem(BaseModel):
    subtitles_name: str
    file_getter: str
    subtitles_directory: str

class BackgroundMusicItem(BaseModel):
    audio_name: str
    file_getter: str
    start_time: int
    duration: int
class VideoRequest(BaseModel):
    tema: str
    usuario: str
    idioma: str
    personaje: str
    script: str
    audio_item: List[AudioItem]
    subtitle_item: List[SubtitleItem]
    author: str
    gameplay_name: str
    background_music: List[BackgroundMusicItem]
    images: List[ImageItem]
    random_images: bool
    random_amount_images: int
    gpt_model: str
    url: str
    status: str

class MinioRequest(BaseModel):
    video_name: str

class UserId(BaseModel):
    user_id: str

@mongo_router.post("/get-videos-user")
async def get_videos_from_user(
    user_id: UserId, db: AsyncIOMotorDatabase = Depends(get_db)
):
    try:
        filter = {"usuario": user_id.user_id}

        # TODO: acá habría que hacer lo de request
        collection_videos = db.videos
        cursor = collection_videos.find(filter, {"_id": False})
        data = await cursor.to_list(length=None)
        return JSONResponse(
            content={
                "videos": data,
                "message": f"Se encontraron {len(data)} videos para el usuario {user_id}",
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as ex:
        print("❌ Error al obtener los videos del usuario:", ex)
        return JSONResponse(
            content={"message": "Error interno del servidor"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@mongo_router.post("/get-videos-url")
async def get_videos_url(user_id: UserId, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        # TODO: acá habría que hacer lo de request
        collection_videos = db.videos

        filter = {
            "usuario": user_id.user_id,
            "$or": [{"DOWNLOADED": {"$exists": False}}, {"DOWNLOADED": False}],
        }


        # TODO: acá habría que hacer lo de request
        projection = {"_id": False, "url": True, "DOWNLOADED": True}
        cursor = collection_videos.find(filter, projection)
        videos_to_download = await cursor.to_list(length=None)

        if not videos_to_download:
            return JSONResponse(
                content={"urls": [], "message": "No hay videos nuevos para descargar."},
                status_code=status.HTTP_200_OK,
            )
        
        urls = [video["url"] for video in videos_to_download]

        await collection_videos.update_many(
            {"usuario": user_id.user_id, "url": {"$in": urls}},
            {"$set": {"DOWNLOADED": True}},
        )

        return JSONResponse(
            content={
                "urls": videos_to_download,
                "message": f"Se encontraron {len(videos_to_download)} videos nuevos para descargar.",
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        return JSONResponse(
            content={
                "message": "Error al obtener o actualizar videos",
                "error": str(e),
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@mongo_router.post("/add-video")
async def add_video(video: VideoRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    
    print("Recibida solicitud para /add-video")
    print("Payload recibido:")
    print(video.model_dump())

    try:
        data = {
            "tema": video.tema,
            "usuario": video.usuario,
            "idioma": video.idioma,
            "personaje": video.personaje,
            "script": video.script,
            "audio_item": [audio.model_dump() for audio in video.audio_item],
            "subtitle_item": [
                subtitle.model_dump() for subtitle in video.subtitle_item
            ],
            "author": video.author,
            "gameplay_name": video.gameplay_name,
            "background_music": [
                music.model_dump() for music in video.background_music
            ],
            "images": [image.model_dump() for image in video.images],
            "random_images": video.random_images,
            "random_amount_images": video.random_amount_images,
            "gpt_model": video.gpt_model,
            "url": video.url,
            "status": video.status,
        }

        print("🛠 Datos procesados para insertar en MongoDB:")
        print(data)

        # TODO: acá habría que hacer lo de request
        collection_videos = db.videos
        result = await collection_videos.insert_one(data)

        print(f"✅ Documento insertado con _id: {result.inserted_id}")

        return JSONResponse(
            content={
                "inserted_id": str(result.inserted_id),
                "message": "Video insertado correctamente",
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        print("❌ Error durante la inserción en MongoDB:")
        print(e)
        raise HTTPException(status_code=500, detail="Error al insertar en MongoDB")


@mongo_router.post("/get-video")
async def get_video(
    video_name: MinioRequest,
    minio_client: Minio = Depends(get_minio_client_to_sign_signatures),
):
    try:
        url = minio_client.presigned_get_object(
            "videos-homero", video_name.video_name, expires=timedelta(days=7) #Hardcoded!
        )
        return {"url": url}

    except Exception as Ex:
        print("Error al buscar video en minio. Video no encontrado")
        print("Exception: ")
        print(Ex)
