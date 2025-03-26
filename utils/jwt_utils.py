from datetime import datetime, timedelta, timezone
import os
import jwt

ALGORITHM = "HS256"
JWT_KEY = os.getenv("JWT_KEY")

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_KEY, algorithm=ALGORITHM)