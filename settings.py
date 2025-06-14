import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
KAFKA_URL = os.getenv("KAFKA_URL")
