import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017/app_db")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")  # Set this in your environment variables