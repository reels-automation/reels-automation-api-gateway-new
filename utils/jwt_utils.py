from datetime import datetime, timedelta, timezone
import time
import os
import jwt

ALGORITHM = "HS256"
JWT_KEY = os.getenv("JWT_KEY")

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_KEY, algorithm=ALGORITHM)

def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except:
        return {}