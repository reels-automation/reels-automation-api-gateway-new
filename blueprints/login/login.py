from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from services.user_service.user_service_postgres import UserServicePostgres
from services.password_service.password_service_postgres import PasswordServicePostgres
from fastapi.responses import JSONResponse
import jwt
from utils.jwt_utils import create_access_token

login_router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str


@login_router.post("/login")
async def login(data:LoginRequest):

    print("data: ", data)

    username = data.username
    password = data.password

    user_service_postgres = UserServicePostgres()
    password_service_postgres = PasswordServicePostgres()
    
    try:
        user_uuid =  user_service_postgres.get_user_by_name(username)
        login =  password_service_postgres.is_same_password(user_uuid, password)

        if login:
            token_data = {"username": username}
            access_token = create_access_token(token_data)
            return (access_token), 201
        else:
            return JSONResponse(content={"message": f"Erorr. Credenciales Incorrectas."},status_code=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        print("Error: " , str(e))
        return JSONResponse(content={"message": f"Error inesperado {str(e)}"}, status_code=status.HTTP_400_BAD_REQUEST)
