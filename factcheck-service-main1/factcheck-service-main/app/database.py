# app/database.py
import motor.motor_asyncio
from .config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_details)
db = client.factcheckdb # You can name your database anything
user_collection = db.get_collection("users")
post_collection = db.get_collection("posts")