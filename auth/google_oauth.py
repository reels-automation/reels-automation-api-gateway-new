from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
import os

from .auth_bearer import JWTBearer
from utils.jwt_utils import create_access_token

google_endpoints = APIRouter()

oauth = OAuth()
oauth.register(
    name='google',
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
async def google_auth_callback(request: Request):
    print("Callback cookies:", request.cookies)
    print("Session at callback:", request.session)
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)

    access_token = create_access_token({
        "sub": user.get("sub"),
        "username": user.get("name")
    })

    return JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"},
        status_code=status.HTTP_200_OK,
    )