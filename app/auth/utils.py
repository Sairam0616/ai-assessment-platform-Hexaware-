from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.database import admin_collection, candidate_collection, educator_collection
from app.config import SECRET_KEY
from smtplib import SMTP_SSL
from email.mime.text import MIMEText

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token retrieval
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def authenticate_user(email: str, password: str, collection):
    user = await collection.find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Retrieve user from the database
    user = await candidate_collection.find_one({"email": email})
    if user is None:
        raise credentials_exception
    return user

def send_reset_email(email: str, token: str):
    reset_link = f"http://localhost:3000/dashboard/candidate/forget?token={token}"
    message_content = f"Please click the link below to reset your password:\n{reset_link}"

    # Create the email message
    msg = MIMEText(message_content)
    msg['Subject'] = "Password Reset Request"
    msg['From'] = "aristro841@gmail.com"  # Replace with your email
    msg['To'] = email

    # Send email using SMTP_SSL
    try:
        with SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('aristro841@gmail.com', 'sdtk lbqh zalj zgtc')  # Replace with your email and password
            smtp.sendmail(msg['From'], [msg['To']], msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")
        

def send_reset_email_educator(email: str, token: str):
    reset_link = f"http://localhost:3000/dashboard/educator/forget?token={token}"
    message_content = f"Please click the link below to reset your password:\n{reset_link}"

    # Create the email message
    msg = MIMEText(message_content)
    msg['Subject'] = "Password Reset Request for Educators"
    msg['From'] = "aristro841@gmail.com"  # Replace with your email
    msg['To'] = email

    # Send email using SMTP_SSL
    try:
        with SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('aristro841@gmail.com', 'sdtk lbqh zalj zgtc')  # Replace with your email and password
            smtp.sendmail(msg['From'], [msg['To']], msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")
        
def send_reset_email_admin(email: str, token: str):
    reset_link = f"http://localhost:3000/dashboard/educator/forget?token={token}"
    message_content = f"Please click the link below to reset your password:\n{reset_link}"

    # Create the email message
    msg = MIMEText(message_content)
    msg['Subject'] = "Password Reset Request for Educators"
    msg['From'] = "aristro841@gmail.com"  # Replace with your email
    msg['To'] = email

    # Send email using SMTP_SSL
    try:
        with SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('aristro841@gmail.com', 'sdtk lbqh zalj zgtc')  # Replace with your email and password
            smtp.sendmail(msg['From'], [msg['To']], msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")
