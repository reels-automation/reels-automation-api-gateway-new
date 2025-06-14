from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

home_router = APIRouter()


@home_router.get("/")
async def home():
    return "maria"
