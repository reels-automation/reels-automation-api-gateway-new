# login.py

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from services.user_service.user_service_postgres import UserServicePostgres
from services.password_service.password_service_postgres import PasswordServicePostgres
from utils.jwt_utils import create_access_token

login_router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@login_router.post("/login")
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    user_service = UserServicePostgres()
    password_service = PasswordServicePostgres()

    user = await user_service.get_user_by_name(db, data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    login_success = await password_service.is_same_password(db, user.id, data.password)
    if not login_success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error. Credenciales incorrectas."
        )

    token_data = {
        "sub": str(user.id),
        "username": user.name,
    }
    access_token = create_access_token(token_data, expires_delta=timedelta(hours=1))

    return JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"},
        status_code=status.HTTP_200_OK
    )
