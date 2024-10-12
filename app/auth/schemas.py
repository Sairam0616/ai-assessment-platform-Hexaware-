from pydantic import BaseModel, EmailStr

class AdminLoginSchema(BaseModel):
    email: EmailStr
    password: str

class CandidateRegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "candidate"  # Default role
    status: bool = False  # Default status

class CandidateLoginSchema(BaseModel):
    email: EmailStr
    password: str
class EducatorLoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenSchema(BaseModel):
    access_token: str
    token_type: str



