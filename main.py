from fastapi import APIRouter, FastAPI
from blueprints.login.login import login_router
from blueprints.register.register import register_router

app = FastAPI()
app.include_router(login_router)
app.include_router(register_router)