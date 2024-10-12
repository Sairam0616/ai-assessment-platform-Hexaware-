from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import secrets
from passlib.context import CryptContext
from app.database import candidate_collection, educator_collection, admin_collection # Modify based on your user collection
from app.auth.utils import send_reset_email, send_reset_email_admin, send_reset_email_educator  # A utility function to send emails

router = APIRouter()

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# candidate==========================================================================candidate
# Model for Forgot Password request
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

# Model for Reset Password request
class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

# Forgot Password Route
@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, background_tasks: BackgroundTasks):
    user = await candidate_collection.find_one({"email": request.email})

    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    # Generate reset token and expiry time
    reset_token = secrets.token_urlsafe(32)
    reset_token_expiry = datetime.utcnow() + timedelta(minutes=15)

    # Update user in database with reset token and expiry
    await candidate_collection.update_one(
        {"email": request.email},
        {"$set": {"reset_token": reset_token, "reset_token_expiry": reset_token_expiry}}
    )

    # Send reset email in the background
    background_tasks.add_task(send_reset_email, request.email, reset_token)

    return {"message": "Password reset link has been sent to your email."}

# Reset Password Route
@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest):
    user = await candidate_collection.find_one({"reset_token": request.token})

    # Validate the token and check expiry
    if not user or user.get("reset_token_expiry") < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # Hash the new password
    hashed_password = pwd_context.hash(request.new_password)

    # Update the password and remove reset token
    await candidate_collection.update_one(
        {"reset_token": request.token},
        {"$set": {"password": hashed_password, "reset_token": None, "reset_token_expiry": None}}
    )

    return {"message": "Password has been reset successfully."}


#educator======================================================================

# Model for Educator Forgot Password request
class EducatorForgotPasswordRequest(BaseModel):
    email: EmailStr

# Model for Educator Reset Password request
class EducatorResetPasswordRequest(BaseModel):
    token: str
    new_password: str

# Educator Forgot Password Route
@router.post("/educator/forgot-password")
async def educator_forgot_password(request: EducatorForgotPasswordRequest, background_tasks: BackgroundTasks):
    educator = await educator_collection.find_one({"email": request.email})

    if not educator:
        raise HTTPException(status_code=404, detail="Email not found")

    # Generate reset token and expiry time
    reset_token = secrets.token_urlsafe(32)
    reset_token_expiry = datetime.utcnow() + timedelta(minutes=15)

    # Update educator in database with reset token and expiry
    await educator_collection.update_one(
        {"email": request.email},
        {"$set": {"reset_token": reset_token, "reset_token_expiry": reset_token_expiry}}
    )

    # Send reset email in the background
    background_tasks.add_task(send_reset_email_educator, request.email, reset_token)

    return {"message": "Password reset link has been sent to your email."}

# Educator Reset Password Route
@router.post("/educator/reset-password")
async def educator_reset_password(request: EducatorResetPasswordRequest):
    educator = await educator_collection.find_one({"reset_token": request.token})

    # Validate the token and check expiry
    if not educator or educator.get("reset_token_expiry") < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # Hash the new password
    hashed_password = pwd_context.hash(request.new_password)

    # Update the password and remove reset token
    await educator_collection.update_one(
        {"reset_token": request.token},
        {"$set": {"password": hashed_password, "reset_token": None, "reset_token_expiry": None}}
    )

    return {"message": "Password has been reset successfully."}

#admin=====================================================================================admin

# Model for Admin Forgot Password request
class AdminForgotPasswordRequest(BaseModel):
    email: EmailStr

# Model for Admin Reset Password request
class AdminResetPasswordRequest(BaseModel):
    token: str
    new_password: str

# Admin Forgot Password Route
@router.post("/admin/forgot-password")
async def admin_forgot_password(request: AdminForgotPasswordRequest, background_tasks: BackgroundTasks):
    admin = await admin_collection.find_one({"email": request.email})

    if not admin:
        raise HTTPException(status_code=404, detail="Email not found")

    # Generate reset token and expiry time
    reset_token = secrets.token_urlsafe(32)
    reset_token_expiry = datetime.utcnow() + timedelta(minutes=15)

    # Update admin in database with reset token and expiry
    await admin_collection.update_one(
        {"email": request.email},
        {"$set": {"reset_token": reset_token, "reset_token_expiry": reset_token_expiry}}
    )

    # Send reset email in the background
    background_tasks.add_task(send_reset_email_admin, request.email, reset_token)

    return {"message": "Password reset link has been sent to your email."}

# Admin Reset Password Route
@router.post("/admin/reset-password")
async def admin_reset_password(request: AdminResetPasswordRequest):
    admin = await admin_collection.find_one({"reset_token": request.token})

    # Validate the token and check expiry
    if not admin or admin.get("reset_token_expiry") < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # Hash the new password
    hashed_password = pwd_context.hash(request.new_password)

    # Update the password and remove reset token
    await admin_collection.update_one(
        {"reset_token": request.token},
        {"$set": {"password": hashed_password, "reset_token": None, "reset_token_expiry": None}}
    )

    return {"message": "Password has been reset successfully."}
