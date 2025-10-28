import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
KAFKA_URL = os.getenv("KAFKA_URL")
VALKEY_URL = os.getenv("VALKEY_URL")

if len(VALKEY_URL) == 0:
    print("VALKEY URL ESTA VACIO: \n", VALKEY_URL)
    