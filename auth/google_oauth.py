from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
import os

from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI

router = APIRouter()

# OAuth config
config_data = {
    'GOOGLE_CLIENT_ID': os.getenv("GOOGLE_CLIENT_ID"),
    'GOOGLE_CLIENT_SECRET': os.getenv("GOOGLE_CLIENT_SECRET"),
}
config = Config(environ=config_data)

oauth = OAuth(config)
oauth.register(
    name='google',
    client_id=config_data['GOOGLE_CLIENT_ID'],
    client_secret=config_data['GOOGLE_CLIENT_SECRET'],
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@router.get("/auth/google/login")
async def login_via_google(request: Request):
    redirect_uri = request.url_for('google_auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/google/callback")
async def google_auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    return {"user": user}

@router.get("/auth/google/logout")
async def google_logout(request: Request):
    request.session.pop('user', None)
    return {"message": "Logged out"}
