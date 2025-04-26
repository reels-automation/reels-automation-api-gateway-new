from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from services.user_service.user_service_postgres import UserServicePostgres
from services.password_service.password_service_postgres import PasswordServicePostgres

from services.user_service.user_service_postgres import UserServicePostgres
from services.user_roles_service.user_roles_service_postgres import UserRolesServicePostgres
from services.roles_service.roles_service_postgres import RolesServicePostgres

from auth.auth_bearer import JWTBearer

from kafka.kafka_producer import KafkaProducerSingleton
from utils.jwt_utils import decode_jwt
from typing import List

create_video_router = APIRouter()

class ImageItem(BaseModel):
    image_name: str
    image_modifier:str
    file_getter: str
    image_directory: str
    timestamp: int
    duration: int

class AudioItem(BaseModel):
    tts_audio_name: str 
    tts_audio_directory:str
    file_getter:str
    pitch:int
    tts_voice:str
    tts_rate:int
    pth_voice:str

class SubtitleItem(BaseModel):
    subtitles_name:str
    file_getter:str
    subtitles_directory:str

class BackgroundMusicItem(BaseModel):
    audio_name:str
    file_getter:str
    start_time:int
    duration:int

class VideoRequest(BaseModel):
    tema:str 
    usuario:int
    idioma:str
    personaje:str
    script:str
    audio_item:List[AudioItem]
    subtitle_item:List[SubtitleItem]
    author:str
    gameplay_name:str
    background_music:List[BackgroundMusicItem]
    images: List[ImageItem]
    random_images: bool
    random_amount_images:int


@create_video_router.post("/create-video", dependencies=[Depends(JWTBearer())])
async def create_video(video:VideoRequest, token: dict = Depends(JWTBearer())):

    user_service_postgress = UserServicePostgres()
    user_roles_services = UserRolesServicePostgres()
    roles_service = RolesServicePostgres()

    decoded_token = decode_jwt(token)
    username = decoded_token["username"]

    user = user_service_postgress.get_user_by_name(username)
    user_role = user_roles_services.get_role_from_user_uuid(user.id)
    current_user_role = roles_service.get_role_name_by_uuid(user_role.role_id)

    
    if current_user_role not in roles_service.get_premium_roles():
        if not user_service_postgress.can_make_post(username):
            return JSONResponse(content={"message":"You don't have enough credits"}, status_code=400)
        
        user_service_postgress.decrease_user_token(username)

    data = {
        "tema": video.tema,
        "usuario": video.tema,
        "idioma": video.idioma,
        "personaje": video.personaje,
        "script": video.script,
        "audio_item": video.audio_item,
        "subtitle_item": video.subtitle_item,
        "author": video.author,
        "gameplay_name":video.gameplay_name,
        "background_music":video.background_music,
        "images":video.images,
        "random_images":False,
        "random_amount_images":0

    }
    kafka_producer = KafkaProducerSingleton()
    topic = "temas"
    key="temas_input_humano"
    value=str(data)

    kafka_producer.produce_message(topic=topic, key=key, value=value)

    
    
        
    return JSONResponse(content={"message":"Processing video creation request"}, status_code=200)
