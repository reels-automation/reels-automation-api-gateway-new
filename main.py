from fastapi import APIRouter, FastAPI
from blueprints.login.login import login_router

app = FastAPI()
app.include_router(login_router)