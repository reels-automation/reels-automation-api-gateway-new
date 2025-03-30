from pydantic import BaseModel
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
    tts_rate:int
    pth_voice:str
    gameplay_name:str
    instagram_account:str

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
        "instagram_account":video.instagram_account,
        "gameplay_name": video.gameplay_name
    }
    kafka_producer = KafkaProducerSingleton()
    topic = "temas"
    key="temas_input_humano"
    value=str(data)

    kafka_producer.produce_message(topic=topic, key=key, value=value)

    
    
        
    return JSONResponse(content={"message":"Processing video creation request"}, status_code=200)
