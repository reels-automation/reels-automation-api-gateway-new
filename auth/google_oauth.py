from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import os
from services.user_service.user_service_postgres import UserServicePostgres

from .oauth2_utils import oauth
from utils.jwt_utils import create_access_token

google_endpoints = APIRouter()

# Route to initiate login with Google
@google_endpoints.get("/auth/google/login")
async def login_via_google(request: Request):
    print("Login cookies:", request.cookies)
    print("Session at login:", request.session)
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    print(f"Redirecting to Google with redirect URI: {redirect_uri}")
    return await oauth.google.authorize_redirect(request, redirect_uri)

# Route to handle callback from Google OAuth
@google_endpoints.get("/auth/google/callback")
async def google_auth_callback(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        user_service = UserServicePostgres()

        print("Callback cookies:", request.cookies)
        print("Session at callback:", request.session)

        # Get the token from the Google response
        token = await oauth.google.authorize_access_token(request)
        print("Token received:", token)  # Log the full token object

        """
        # Parse the ID token
        user_google = await oauth.google.parse_id_token(request, token)
        print("Parsed User Google Data:", user_google)  # Log parsed user data
        """

        print("ESPERANDO \n\n\n\n\n")

        # Check if the user exists in the database
        if not await user_service.user_exists(db, token["userinfo"]["name"], token["userinfo"]["email"]):
            print("User not found, creating new user.")
            user = await user_service.create_user(db, token["userinfo"]["name"], token["userinfo"]["email"])
        else:
            print("User found, retrieving user.")
            user = await user_service.get_user_by_email(db, token["userinfo"]["email"])

        # Log the user data
        print("User found or created:", user)

        # Create an access token for the logged-in user
        access_token = create_access_token({
            "sub": str(user.id),
            "username": user.name
        })
        print("Access token generated:", access_token)

        # Redirect to frontend with the access token
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
        redirect_url = f"{frontend_url}/oauth-callback?token={access_token}"
        print(f"Redirecting to frontend with token: {access_token}")
        
        return RedirectResponse(url=redirect_url)
    except Exception as e:
        # Log the error details if the OAuth process fails
        print("Google OAuth callback error:", e)
        return JSONResponse(
            content={"detail": "Google OAuth failed", "error": str(e)},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
