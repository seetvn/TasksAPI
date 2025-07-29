from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError
from models import User
from database import async_session
from sqlmodel import select
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

SECRET_KEY = os.environ["SECRET"]
ALGORITHM = os.environ["ALGORITHM"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Retrieve the current user based on the provided JWT token.

    Args:
        token (str): JWT token from the request.

    Returns:
        User: The authenticated user object.

    Raises:
        HTTPException: If authentication fails due to missing token, invalid token,
                       expired token, or user not found.
    """
    print("TOKEN RECEIVED:", token)

    # Check if token is provided
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        # Ensure username is present in token payload
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is valid but missing username (sub)",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except ExpiredSignatureError:
        # Handle expired token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        # Handle invalid token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Retrieve user from database
    async with async_session() as session:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        # Check if user exists
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found for given token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user
