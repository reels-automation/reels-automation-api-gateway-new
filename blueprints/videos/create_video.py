from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from services.user_service.user_service_postgres import UserServicePostgres
from services.password_service.password_service_postgres import PasswordServicePostgres
from services.user_roles_service.user_roles_service_postgres import UserRolesServicePostgres
from services.roles_service.roles_service_postgres import RolesServicePostgres
from auth.auth_bearer import JWTBearer

from server_base import app_producer

create_video_router = APIRouter()

class VideoRequest(BaseModel):
    tema:str
    personaje:str
    script:str
    tts_audio_name:str
    tts_audio_bucket:str
    subtitles_name:str
    subtitles_bucket:str
    author:str
    pitch:int
    tts_voice:str
    tts_rate:str
    pth_voice:str
    instagram_account:str
    gameplay_name:str

@create_video_router.post("/create-video", dependencies=[Depends(JWTBearer())])
async def create_video(video:VideoRequest):
    
    data = {
        "tema": video.tema,
        "personaje": video.personaje,
        "script": video.script,
        "tts_audio_name": video.tts_audio_name,
        "tts_audio_bucket": video.tts_audio_bucket,
        "subtitles_name": video.subtitles_name,
        "subtitles_bucket": video.subtitles_bucket,
        "author": video.author,
        "pitch": video.pitch,
        "tts_voice": video.tts_voice,
        "tts_rate": video.tts_rate,
        "pth_voice": video.pth_voice,
        "instagram_account": video.instagram_account,
        "gameplay_name": video.gameplay_name
    }

    with app_producer.get_producer() as producer:
        producer.produce(
            topic="temas", key="temas_input_humano", value=str(data)
        )
    
    return JSONResponse(content={"message":"Processing video creation request"}, status_code=200)
