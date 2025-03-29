from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from services.user_service.user_service_postgres import UserServicePostgres
from services.password_service.password_service_postgres import PasswordServicePostgres
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta, timezone
from utils.jwt_utils import create_access_token

login_router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str


@login_router.post("/login")
async def login(data:LoginRequest):
    username = data.username
    password = data.password

    user_service_postgres = UserServicePostgres()
    password_service_postgres = PasswordServicePostgres()
    
    try:
        user =  user_service_postgres.get_user_by_name(username)
        login =  password_service_postgres.is_same_password(user.id, password)

        if login:
            token_data = {
            "sub": str(user.id),
            "username": user.name
            }
            access_token = create_access_token(token_data, expires_delta=timedelta(hours=1))

            return JSONResponse(
                content={
                    "access_token": access_token,
                    "token_type": "bearer"
                },
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(content={"message": f"Erorr. Credenciales Incorrectas."},status_code=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        return JSONResponse(content={"message": f"Error inesperado {str(e)}"}, status_code=status.HTTP_400_BAD_REQUEST)
