# app/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database
from app.config import DATABASE_URL

# Initialize MongoDB client
client = AsyncIOMotorClient(DATABASE_URL)
database: Database = client["app_db"]

# Collections for different user types
admin_collection = database.get_collection("admins")
candidate_collection = database.get_collection("candidates")
educator_collection = database.get_collection("educators")
assessment_collection = database.get_collection("assessments")  # New assessments collection
status_collection=database.get_collection("status")
results_collection=database.get_collection("results")
session_collection=database.get_collection("session")

# Function to create indexes
async def create_indexes():
    await admin_collection.create_index("email", unique=True)
    await candidate_collection.create_index("email", unique=True)
    await educator_collection.create_index("email", unique=True)
    await assessment_collection.create_index("email")  # Index for educator email
    await status_collection.create_index("email")
    await results_collection.create_index("email")
    await session_collection.create_index("email")