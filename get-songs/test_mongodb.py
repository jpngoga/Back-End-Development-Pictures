import os
import certifi
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DATABASE = os.getenv("MONGO_DATABASE")

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=15000
)

try:
    client.admin.command("ping")
    print("SUCCESS: Connected to MongoDB Atlas!")

    db = client[MONGO_DATABASE]
    print("Database:", db.name)

except Exception as error:
    print("Connection failed:", error)

finally:
    client.close()