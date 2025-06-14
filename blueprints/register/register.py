from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from pydantic import BaseModel

from database import get_db
from services.user_service.user_service_postgres import UserServicePostgres
from services.password_service.password_service_postgres import PasswordServicePostgres
from services.user_roles_service.user_roles_service_postgres import (
    UserRolesServicePostgres,
)
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
    user_service = UserServicePostgres()
    password_service = PasswordServicePostgres()
    user_roles_service = UserRolesServicePostgres()
    roles_service = RolesServicePostgres()

    async with db.begin():

        if len(data.username) > 15:
            raise HTTPException(
                status_code=400,
                detail="El nombre de usuario no puede tener más de 15 caracteres",
            )

        existing_user = await user_service.get_user_by_name(db, data.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Nombre de usuario ya tomado")

        existing_email = await user_service.get_user_by_email(db, data.email)
        if existing_email:
            raise HTTPException(status_code=400, detail="Email ya registrado")

        new_user = await user_service.create_user(db, data.username, data.email)

        await password_service.create_password(db, new_user.id, data.password)

        role_id = await roles_service.get_role_by_name(db, "User")

        await user_roles_service.create_user_role(db, role_id, new_user.id)

    await db.refresh(new_user)
    token_data = {
        "sub": str(new_user.id),
        "username": new_user.name,
    }
    access_token = create_access_token(token_data, expires_delta=timedelta(weeks=24))

    return JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"},
        status_code=status.HTTP_201_CREATED,
    )
