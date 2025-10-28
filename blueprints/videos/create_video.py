# create_video.py

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db
from services.user_service.user_service_postgres import UserServicePostgres
from services.roles_service.roles_service_postgres import RolesServicePostgres
from services.user_roles_service.user_roles_service_postgres import (
    UserRolesServicePostgres,
)
from services.valkey_service.valkey_service import ValkeyClient
from auth.auth_bearer import JWTBearer
from kafka.kafka_producer import KafkaProducerSingleton
from utils.jwt_utils import decode_jwt
from pydantic import BaseModel
from settings import VALKEY_URL

create_video_router = APIRouter()


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


@create_video_router.post("/create-video", dependencies=[Depends(JWTBearer())])
async def create_video(
    video: VideoRequest,
    token: dict = Depends(JWTBearer()),
    db: AsyncSession = Depends(get_db),
):
    print("Evidi well")
    user_service = UserServicePostgres()
    user_roles_service = UserRolesServicePostgres()
    roles_service = RolesServicePostgres()

    decoded_token = decode_jwt(token)
    username = decoded_token["username"]
    sub = decoded_token["sub"]

    async with db.begin():  # single transaction for credit check + decrement
        user = await user_service.get_user_by_name(db, username)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        current_user_role = await user_roles_service.get_role_from_user_uuid(
            db, user.id
        )

        if current_user_role not in await roles_service.get_premium_roles(db):
            if not await user_service.can_make_post(db, sub):
                raise HTTPException(status_code=400, detail="Creditos insuficientes")
            await user_service.decrease_user_token(db, username)

    # transaction committed; now fire off Kafka
    data = {
        "tema": video.tema,
        "usuario": video.usuario,
        "idioma": video.idioma,
        "personaje": video.personaje,
        "script": video.script,
        "audio_item": [audio.model_dump() for audio in video.audio_item],
        "subtitle_item": [subtitle.model_dump() for subtitle in video.subtitle_item],
        "author": video.author,
        "gameplay_name": video.gameplay_name,
        "background_music": [music.model_dump() for music in video.background_music],
        "images": [image.model_dump() for image in video.images],
        "random_images": video.random_images,
        "random_amount_images": video.random_amount_images,
        "gpt_model": video.gpt_model,
    }

    try:
        KafkaProducerSingleton.produce_message(
            topic="temas", key="temas_input_humano", value=str(data)
        )
        
        valkey_client = ValkeyClient(VALKEY_URL)
        key = f"video:{video.usuario}_{video.tema}"
        valkey_client.insert_video(key,data)
        valkey_client.change_status(key, "IN PROGRESS")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error del servidor: {e}")

    return JSONResponse(
        content={"message": "Processing video creation request"},
        status_code=status.HTTP_200_OK,
    )


@create_video_router.get("/get-videos-status")
async def get_video_status():
    try: 
        valkey_client = ValkeyClient(VALKEY_URL)
        videos = valkey_client.get_all_videos()
        return videos
    except Exception as ex: 
        print("Exceptional hacer get de los videos de valkey")
        