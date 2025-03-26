from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from blueprints.login.login import login_router
from blueprints.register.register import register_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/"],  # Puedes restringirlo a dominios específicos en producción
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

app.include_router(login_router)
app.include_router(register_router)
