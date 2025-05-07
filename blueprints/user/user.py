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

user_router = APIRouter()

class RegisterRequest(BaseModel):
    user_id: str

@user_router.post("/user-tokens")
async def get_user_tokens(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    user_service = UserServicePostgres()


    async with db.begin():            
        try:
            print("aaaaaaaaaaaaaaaaaaaaaaaaaAAAAaa: " , data.user_id)
            credits = await user_service.get_user_credits(db, data.user_id)
        except:
            return JSONResponse(
            content={"Bad request": str(data.user_id)},
            status_code=status.HTTP_202_ACCEPTED)
        
    return JSONResponse(
        content={"credits": int(credits)},
        status_code=status.HTTP_202_ACCEPTED
    )
