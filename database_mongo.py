import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["reels_automation"]
collection_temas = db.temas
collection_videos = db.videos

async def get_db():
    yield db
    

