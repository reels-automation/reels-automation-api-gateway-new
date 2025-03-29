from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from utils.jwt_utils import decode_jwt

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        print("Received ! ")

        print("Request: ", request.json())
        body_bytes = await request.body()
        print("Request body (bytes): ", body_bytes)
        print("Headers: ", request.headers.get("authorization"))

        credentials = request.headers.get("authorization")
        #credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        print("Headers: ", credentials)

        if credentials:
            if not credentials.startswith("Bearer"):
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")

            token = credentials.split(" ")[1]

            print(token)

            if not self.verify_jwt(token):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return token
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True

        return isTokenValid
