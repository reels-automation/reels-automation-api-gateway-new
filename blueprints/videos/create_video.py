from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from services.user_service.user_service_postgres import UserServicePostgres
from services.password_service.password_service_postgres import PasswordServicePostgres
from services.user_roles_service.user_roles_service_postgres import UserRolesServicePostgres
from services.roles_service.roles_service_postgres import RolesServicePostgres
from auth.auth_bearer import JWTBearer

create_video_router = APIRouter()

class VideoRequest(BaseModel):
    topic:str

@create_video_router.post("/create-video", dependencies=[Depends(JWTBearer())])
async def create_video(video:VideoRequest):
    return JSONResponse(content={"message":"data"})
