from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from services.user_service.user_service_postgres import UserServicePostgres
from services.password_service.password_service_postgres import PasswordServicePostgres
from services.user_roles_service.user_roles_service_postgres import UserRolesServicePostgres
from services.roles_service.roles_service_postgres import RolesServicePostgres
from datetime import datetime, timedelta, timezone
from utils.jwt_utils import create_access_token


register_router = APIRouter()

class RegisterRequest(BaseModel):
    username:str
    email:str
    password:str


@register_router.post("/register")
async def register(data:RegisterRequest):

    username = data.username
    email = data.email
    password = data.password

    user_service_postgres = UserServicePostgres()
    password_service_postgres = PasswordServicePostgres()
    user_roles_service_postgres = UserRolesServicePostgres()
    roles_service_postgres = RolesServicePostgres()

    new_user = user_service_postgres.create_user(username, email)
    password_service_postgres.create_password(new_user.id, password)
    rol_id = roles_service_postgres.get_role_by_name("User")
    user_roles_service_postgres.create_user_role(rol_id, new_user.id)
    
    token_data = {
        "sub": str(new_user.id),
        "username": new_user.name,
        "role": "User"
    }

    access_token = create_access_token(token_data, expires_delta=timedelta(hours=1))

    return JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"},
        status_code=status.HTTP_201_CREATED
    )
