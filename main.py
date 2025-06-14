"""
Main entry point for the FastAPI application.
This file initializes the FastAPI app, sets up CORS middleware, and includes the routers for different blueprints.
"""
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from blueprints.login.login import login_router
from blueprints.register.register import register_router
from blueprints.home.home import home_router
from blueprints.videos.create_video import create_video_router
from blueprints.mongo.mongo import mongo_router
from blueprints.mercadopago_api.mercadopago_api import mercadopago_router
from blueprints.user.user import user_router

from database import Base, engine
from utils.utils import create_default_roles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringirlo a dominios específicos en producción
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

app.include_router(login_router)
app.include_router(register_router)
app.include_router(home_router)
app.include_router(create_video_router)
app.include_router(mongo_router)
app.include_router(mercadopago_router)
app.include_router(user_router)




@app.on_event("startup")
async def startup():
    if os.getenv("ENVIRONMENT") == "DEVELOPMENT":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    await create_default_roles()
