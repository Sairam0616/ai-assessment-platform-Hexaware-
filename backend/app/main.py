from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as auth_router
from app.routes import router as api_router

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

# Include routers
app.include_router(auth_router)
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-Assessment Platform"}
