import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from settings import MONGO_URL


client = AsyncIOMotorClient(MONGO_URL)
db = client["reels_automation"]
collection_temas = db.temas
collection_videos = db.videos

async def get_db():
    yield db
    

