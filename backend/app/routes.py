from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import authenticate_user, create_access_token, get_password_hash
from app.schemas import AdminLoginSchema, CandidateRegisterSchema, CandidateLoginSchema, EducatorLoginSchema, TokenSchema
from app.database import admin_collection, candidate_collection, educator_collection

router = APIRouter()

@router.post("/auth/admin/login", response_model=TokenSchema)
async def login_admin(admin_data: AdminLoginSchema):
    admin = await authenticate_user(admin_data.email, admin_data.password, admin_collection)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": admin['email']})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auth/candidate/register", response_model=TokenSchema)
async def register_candidate(candidate_data: CandidateRegisterSchema):
    existing_candidate = await candidate_collection.find_one({"email": candidate_data.email})
    if existing_candidate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )
    candidate_data.password = get_password_hash(candidate_data.password)
    new_candidate = await candidate_collection.insert_one(candidate_data.dict())
    access_token = create_access_token(data={"sub": candidate_data.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auth/candidate/login", response_model=TokenSchema)
async def login_candidate(candidate_data: CandidateLoginSchema):
    candidate = await authenticate_user(candidate_data.email, candidate_data.password, candidate_collection)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": candidate['email']})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auth/educator/login", response_model=TokenSchema)
async def login_educator(educator_data: EducatorLoginSchema):
    educator = await authenticate_user(educator_data.email, educator_data.password, educator_collection)
    if not educator:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": educator['email']})
    return {"access_token": access_token, "token_type": "bearer"}
