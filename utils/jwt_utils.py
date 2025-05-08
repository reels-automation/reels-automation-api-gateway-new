from datetime import datetime, timedelta, timezone
import os
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

ALGORITHM = "HS256"
JWT_KEY = os.getenv("JWT_KEY")

if not JWT_KEY:
    raise ValueError("JWT_KEY environment variable is not set")

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_KEY, algorithm=ALGORITHM)

def decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        # no debería estar en producción así
        print("Token has expired")
    except InvalidTokenError:
        # no debería estar en producción así
        print("Invalid token")
    return {}
