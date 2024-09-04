from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database

client = AsyncIOMotorClient("mongodb://localhost:27017")
database: Database = client["app_db"]

admin_collection = database.get_collection("admins")
candidate_collection = database.get_collection("candidates")
educator_collection = database.get_collection("educators")

async def create_indexes():
    await admin_collection.create_index("email", unique=True)
    await candidate_collection.create_index("email", unique=True)
    await educator_collection.create_index("email", unique=True)

