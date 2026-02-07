from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlmodel import select
from uuid import UUID
import os
from .database import get_async_session
from ..models.user import User, UserRead
from sqlalchemy.ext.asyncio import AsyncSession


# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize JWT scheme - HTTPBearer returns 403 by default, but we want 401 for auth issues
security = HTTPBearer()

from .config import settings

# Use settings from the config
SECRET_KEY = settings.better_auth_secret
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[UUID] = None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    """
    return pwd_context.hash(password)


async def authenticate_user(session: AsyncSession, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.
    """
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    user = result.scalars().first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with optional expiration.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """
    Verify a JWT token and return the decoded data.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("user_id")

        if username is None or user_id is None:
            return None

        token_data = TokenData(username=username, user_id=UUID(user_id))
        return token_data
    except JWTError:
        return None


async def get_current_user_from_cookie(request: Request, session: AsyncSession = Depends(get_async_session)) -> UserRead:
    """
    Get the current authenticated user from the JWT token in the cookie.
    This is a pure cookie-based authentication dependency that does NOT rely on OAuth2PasswordBearer.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Extract token directly from cookies - this is the core of cookie-based auth
    token = request.cookies.get("access_token")
    if not token:
        # Log the missing cookie for debugging
        print(f"DEBUG: No access_token cookie found in request. Available cookies: {request.cookies.keys()}")
        raise credentials_exception

    token_data = verify_token(token)
    if token_data is None:
        # Log invalid token for debugging
        print(f"DEBUG: Invalid access_token in cookie")
        raise credentials_exception

    statement = select(User).where(User.id == token_data.user_id)
    result = await session.execute(statement)
    user = result.scalars().first()

    if user is None:
        print(f"DEBUG: User not found in database for token user_id: {token_data.user_id}")
        raise credentials_exception

    return UserRead.model_validate(user)


def get_current_active_user(current_user: UserRead = Depends(get_current_user_from_cookie)) -> UserRead:
    """
    Get the current active user, ensuring they are active.
    """
    # In this implementation, we assume all users are active
    # In a more complex system, you might check for user status
    return current_user


async def get_user_id_from_cookie(request: Request) -> UUID:
    """
    Extract user ID directly from the JWT token in the cookie without database lookup.
    This is used for authorization checks where we just need the user ID.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = request.cookies.get("access_token")
    if not token:
        raise credentials_exception

    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception

    return token_data.user_id