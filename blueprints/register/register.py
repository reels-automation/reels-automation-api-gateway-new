from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from pydantic import BaseModel

from database import get_db
from services.user_service.user_service_postgres import UserServicePostgres
from services.password_service.password_service_postgres import PasswordServicePostgres
from services.user_roles_service.user_roles_service_postgres import UserRolesServicePostgres
from services.roles_service.roles_service_postgres import RolesServicePostgres
from utils.jwt_utils import create_access_token

register_router = APIRouter()

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

@register_router.post("/register")
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    username = data.username
    email = data.email
    password = data.password

    user_service = UserServicePostgres()
    password_service = PasswordServicePostgres()
    user_roles_service = UserRolesServicePostgres()
    roles_service = RolesServicePostgres()

    existing_user = await user_service.get_user_by_name(db, username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = await user_service.create_user(db, username, email)
    await password_service.create_password(db, new_user.id, password)

    role_id = await roles_service.get_role_by_name(db, "User")
    if not role_id:
        raise HTTPException(status_code=500, detail="Role 'User' not found")
    
    await user_roles_service.create_user_role(db, role_id, new_user.id)

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
