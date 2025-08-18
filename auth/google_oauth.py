from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import os
from services.user_service.user_service_postgres import UserServicePostgres

from .auth_bearer import JWTBearer
from utils.jwt_utils import create_access_token

google_endpoints = APIRouter()

oauth = OAuth()
oauth.register(
    name='google',
    authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@google_endpoints.get("/auth/google/login")
async def login_via_google(request: Request):
    print("Login cookies:", request.cookies)
    print("Session at login:", request.session)
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@google_endpoints.get("/auth/google/callback")
async def google_auth_callback(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        user_service = UserServicePostgres()

        print("Callback cookies:", request.cookies)
        print("Session at callback:", request.session)
        token = await oauth.google.authorize_access_token(request)
        user_google = await oauth.google.parse_id_token(request, token)

        if not await user_service.user_exists(db, user_google.get("name"), user_google.get("email")):
            user = await user_service.create_user(db, user_google.get("name"), user_google.get("email"))
        else:
            user = await user_service.get_user_by_email(db, user_google.get("email"))

        access_token = create_access_token({
            "sub": str(user.id),
            "username": user.name
        })

        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
        redirect_url = f"{frontend_url}/oauth-callback?token={access_token}"
        return RedirectResponse(url=redirect_url)
    except Exception as e:
        print("Google OAuth callback error:", e)
        return JSONResponse(
            content={"detail": "Google OAuth failed", "error": str(e)},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
