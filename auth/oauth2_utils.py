from fastapi.security import OAuth2PasswordBearer
from authlib.integrations.starlette_client import OAuth
import os
from starlette.config import Config

oauth_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or None
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') or None

if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise Exception('Missing env variables')

config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}

starlette_config = Config(environ=config_data)

oauth = OAuth(starlette_config)

oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)