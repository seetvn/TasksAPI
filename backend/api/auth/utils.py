from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt
from models import User
from database import async_session
from sqlmodel import select
from schemas import UserCreate
from fastapi import HTTPException
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
import os


SECRET_KEY = os.environ["SECRET"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict) -> str:
    """
    Generate a JWT access token containing the provided data and an expiration time.

    Args:
        data (dict): The payload data to include in the token.

    Returns:
        str: The encoded JWT access token as a string.

    Note:
        The token will expire after a duration specified by ACCESS_TOKEN_EXPIRE_MINUTES.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def create_user(user: UserCreate):
    """
    Create a new user in the database and return an access token.

    Args:
        user (UserCreate): The user data containing username and password.

    Raises:
        HTTPException: If the username already exists in the database.

    Returns:
        dict: A dictionary containing the access token and its type.

    """
    async with async_session() as session:
        result = await session.execute(select(User).where(User.username == user.username))
        # Check if the username already exists
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username already exists")

        new_user = User(username=user.username, hashed_password=hash_password(user.password))
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        token = create_access_token({"sub": new_user.username})
        return {"access_token": token, "token_type": "bearer"}

async def authenticate_user(user: UserCreate):
    """
    Authenticate a user based on provided credentials.

    Args:
        user (UserCreate): The user credentials containing username and password.

    Returns:
        dict: A dictionary containing the access token and token type.

    Raises:
        HTTPException: If authentication fails due to invalid credentials.

    """
    async with async_session() as session:
        result = await session.execute(select(User).where(User.username == user.username))
        db_user = result.scalar_one_or_none()
        # Check if the user exists and the password is correct
        if not db_user or not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token({"sub": db_user.username})
        return {"access_token": token, "token_type": "bearer"}
    
#TODO: erase after testing
async def get_all_users():
        async with async_session() as session:
            print("=== GETTING ALL USERS ===")
            result = await session.execute(select(User))
            users = result.scalars().all()
            return users