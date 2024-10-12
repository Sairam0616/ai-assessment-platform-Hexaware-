import io
from app.auth.models import PyObjectId
from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from app.database import admin_collection, candidate_collection, educator_collection
from fastapi.responses import StreamingResponse
import pandas as pd
from io import BytesIO, StringIO
import bcrypt 

router = APIRouter()

# User model with stricter validation
class User(BaseModel):
    id: Optional[str]
    username: Optional[str] = Field(None, description="User's username")
    email: Optional[str] = Field(None, description="User's email")
    mobile: Optional[str] = Field(None, description="User's mobile number")
    dob: Optional[str] = Field(None, description="User's date of birth")
    location: Optional[str] = Field(None, description="User's location")
    role: Optional[str] = Field(None, description="User's role")
    status: Optional[str] = Field(default="active", description="User's status")

# Helper function to convert MongoDB document to Pydantic model
def user_from_mongo(user_data):
    return User(
        id=str(user_data["_id"]),
        username=user_data.get("username"),
        email=user_data.get("email"),
        mobile=user_data.get("mobile"),
        dob=user_data.get("dob"),
        location=user_data.get("location"),
        role=user_data.get("role"),
        status=str(user_data.get("status", "active"))
    )

@router.get("/admin/users", response_model=List[User])
async def get_users(
    email: Optional[str] = Query(None, description="Email of the user to fetch"),
    role: Optional[str] = Query(None, description="Role of the user to fetch (admin, candidate, educator, or 'all')")
):
    users = []
    
    # If email is provided, prioritize fetching by email
    if email:
        collections = [admin_collection, candidate_collection, educator_collection]
        for collection in collections:
            user = await collection.find_one({"email": email})
            if user:
                users.append(user_from_mongo(user))
        if not users:
            raise HTTPException(status_code=404, detail="User not found")
    
    # If no email, fetch by role
    elif role:
        collections = {
            "admin": admin_collection,
            "candidate": candidate_collection,
            "educator": educator_collection,
        }
        if role in collections:
            collection = collections[role]
            async for user in collection.find():
                users.append(user_from_mongo(user))
        elif role == "all":
            for collection in collections.values():
                async for user in collection.find():
                    users.append(user_from_mongo(user))
        else:
            raise HTTPException(status_code=400, detail="Invalid role specified")
    
    # If neither email nor role is specified, fetch all users
    else:
        for collection in [admin_collection, candidate_collection, educator_collection]:
            async for user in collection.find():
                users.append(user_from_mongo(user))
    
    return users

# Deactivate user
@router.patch("/admin/users/{email}/deactivate")
async def deactivate_user(email: str):
    user = await admin_collection.find_one({"email": email}) or \
           await candidate_collection.find_one({"email": email}) or \
           await educator_collection.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    role = user.get("role")
    collection = get_collection_by_role(role)
    if collection is None:
        raise HTTPException(status_code=400, detail="Invalid user role")

    result = await collection.update_one({"email": email}, {"$set": {"status": "deactivated"}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found or already deactivated")

    return {"message": "User deactivated successfully", "status": "deactivated"}
@router.patch("/admin/users/{email}/reactivate")
async def reactivate_user(email: str):
    # Check all collections for the user
    user = await admin_collection.find_one({"email": email}) or \
           await candidate_collection.find_one({"email": email}) or \
           await educator_collection.find_one({"email": email})

    # If user not found in any collection
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Determine the user's role and corresponding collection
    role = user.get("role")
    collection = get_collection_by_role(role)
    if collection is None:
        raise HTTPException(status_code=400, detail="Invalid user role")

    # Attempt to update the user's status to active
    result = await collection.update_one({"email": email}, {"$set": {"status": "active"}})
    
    # Check if the update was successful
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found or already active")

    return {"message": "User reactivated successfully", "status": "active"}


# Delete user
@router.delete("/admin/users/{email}")
async def delete_user(email: str):
    collections = [admin_collection, candidate_collection, educator_collection]
    for collection in collections:
        user = await collection.find_one({"email": email})
        if user:
            await collection.delete_one({"email": email})
            return {"message": f"User with email {email} (role: {user.get('role')}) deleted successfully"}
    
    raise HTTPException(status_code=404, detail="User not found")

def get_collection_by_role(role: str):
    if role == "admin":
        return admin_collection
    elif role == "candidate":
        return candidate_collection
    elif role == "educator":
        return educator_collection
    return None

# Import users from CSV
@router.post("/admin/users/import")
async def import_users(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File format not supported. Please upload a CSV file.")
    
    contents = await file.read()
    df = pd.read_csv(StringIO(contents.decode('utf-8')))
    
    required_columns = ['username', 'email', 'role']
    for col in required_columns:
        if col not in df.columns:
            raise HTTPException(status_code=400, detail=f"Missing required column: {col}")

    for _, row in df.iterrows():
        user_data = {
            "username": row['username'],
            "email": row['email'],
            "role": row['role'],
            "status": "active"
        }
        collection = get_collection_by_role(row['role'])
        if collection is not None:
            await collection.insert_one(user_data)

    return {"message": "Users imported successfully"}

# Export users to CSV
@router.get("/admin/users/export")
async def export_users():
    users_data = []

    # List of collections to iterate through (admin, candidate, educator)
    collections = [
        {"collection": admin_collection, "role": "admin"},
        {"collection": candidate_collection, "role": "candidate"},
        {"collection": educator_collection, "role": "educator"}
    ]

    # Loop through each collection and extract only username, email, and role
    for item in collections:
        async for user in item["collection"].find():
            user_data = {
                "username": user.get("username"),
                "email": user.get("email"),
                "role": item["role"]
            }
            users_data.append(user_data)

    # Convert the filtered user data to a DataFrame
    df = pd.DataFrame(users_data)
    
    # Create an in-memory output file for the Excel file
    output = io.BytesIO()
    
    # Write the DataFrame to an Excel file using XlsxWriter
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Users')
    
    # Seek to the beginning of the output
    output.seek(0)

    # Create a StreamingResponse to send the Excel file
    response = StreamingResponse(
        output,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
    # Setting the filename and extension correctly
    response.headers["Content-Disposition"] = "attachment; filename=users_export.xlsx"

    return response
# User Update Model
class UserUpdateModel(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    mobile: Optional[str] = Field(None, description="User's mobile number")
    dob: Optional[str] = Field(None, description="User's date of birth")
    location: Optional[str] = Field(None, description="User's location")
    role: Optional[str] = Field(None, pattern="^(admin|candidate|educator)$")
    status: Optional[str] = Field(None, pattern="^(active|deactivated)$")

# Password hashing
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

@router.put("/admin/users/{email}")
async def update_user(email: str, user_update: UserUpdateModel):
    collections = [admin_collection, candidate_collection, educator_collection]
    user_found = None
    user_collection = None

    # Find the user across all collections using the email
    for collection in collections:
        user_found = await collection.find_one({"email": email})  # Search by email
        if user_found:
            user_collection = collection
            break
    
    if not user_found:
        raise HTTPException(status_code=404, detail="User not found")

    # Prepare fields to update
    update_fields = {k: v for k, v in user_update.dict(exclude_unset=True).items()}

    # Check if role is being updated
    if 'role' in update_fields and update_fields['role'] != user_found['role']:
        new_role = update_fields['role']
        new_collection = get_collection_by_role(new_role)

        if new_collection is None:
            raise HTTPException(status_code=400, detail="Invalid new role specified")

        # Prepare user data for the new collection
        user_data = {**user_found, **update_fields}
        user_data['role'] = new_role  # Update the role

        # Remove the user from the old collection
        await user_collection.delete_one({"email": email})

        # Insert the user into the new collection
        await new_collection.insert_one(user_data)

        # Return a success message
        return {"message": "User role updated and data transferred successfully"}

    # Hash password only if it is provided and not empty
    if 'password' in update_fields and update_fields['password']:
        update_fields['password'] = hash_password(update_fields['password'])
    else:
        update_fields.pop('password', None)  # Remove password from update if not provided

    # Update user in the correct collection
    result = await user_collection.update_one(
        {"email": email},  # Use email for updating
        {"$set": update_fields}
    )
    
    if result.modified_count == 1:
        return {"message": "User updated successfully"}
    else:
        raise HTTPException(status_code=400, detail="User update failed")
