# import os
# from dotenv import load_dotenv

# load_dotenv()

# SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
# DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017/app_db")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.routes import router as auth_router

app = FastAPI()

# Allow CORS for frontend
origins = [
    "http://localhost:3000",  # Your Next.js development server
    "http://your-frontend-domain.com"  # Your production domain if available
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the authentication router
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Hello, AI-Assessment Platform!"}
