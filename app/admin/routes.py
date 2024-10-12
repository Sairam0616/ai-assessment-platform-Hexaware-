from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.auth.utils import get_password_hash
from app.database import admin_collection, candidate_collection, educator_collection

router = APIRouter()

@router.get("/dashboard")
async def get_admin_dashboard():
    return {"message": "Admin Dashboard"}

# Schema for adding a new user
class AddUserSchema(BaseModel):
    username: str
    email: EmailStr
    role: str  # candidate, educator, admin

# Route to add a new user (admin, candidate, educator)
@router.post("/admin/add-user")
async def add_user(user_data: AddUserSchema):
    # Determine the correct collection based on the role
    if user_data.role == "candidate":
        collection = candidate_collection
    elif user_data.role == "educator":
        collection = educator_collection
    elif user_data.role == "admin":
        collection = admin_collection
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role"
        )
    
    # Check if the email is already registered
    existing_user = await collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {user_data.email} is already registered"
        )
    
    # Set the password as the username and hash it
    hashed_password = get_password_hash(user_data.username)
    
    # Insert the new user into the correct collection
    user = {
        "username": user_data.username,
        "email": user_data.email,
        "password": hashed_password,
        "role": user_data.role
    }
    
    await collection.insert_one(user)
    
    return {"message": f"User {user_data.username} added successfully as {user_data.role}"}


