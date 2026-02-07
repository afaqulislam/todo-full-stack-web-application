from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from datetime import timedelta
from ..models.user import UserCreate, UserRead
from ..services.user_service import UserService
from ..core.security import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user_from_cookie
from ..core.database import get_async_session
from pydantic import BaseModel
from ..core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix=f"{settings.api_v1_prefix}/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    *,
    user_create: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Register a new user account.
    """
    try:
        return await UserService.create_user(session=session, user_create=user_create)
    except HTTPException:
        # Re-raise HTTP exceptions from the service
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during user registration"
        )


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login_user(
    response: Response,
    login_request: LoginRequest,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Login with email and password. Sets JWT in HTTP-only cookie.
    """
    user = await authenticate_user(session, login_request.email, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token with user ID and email
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": str(user.id)}, expires_delta=access_token_expires
    )

    # Set the token in an HTTP-only cookie with improved attributes for localhost
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",  # Prevents CSRF attacks - "strict" would be more secure but may cause issues with redirects
        max_age=1800,  # 30 minutes in seconds
        path="/",  # Make cookie available for all paths
        domain=None,  # Use default domain - don't set for localhost to avoid conflicts
    )

    return {"message": "Login successful", "user_id": str(user.id)}


@router.post("/logout")
async def logout_user(response: Response):
    """
    Logout user by clearing the access token cookie.
    """
    response.delete_cookie(
        key="access_token",
        path="/",  # Ensure we're deleting the cookie set for all paths
    )
    return {"message": "Logout successful"}


@router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user: UserRead = Depends(get_current_user_from_cookie)
):
    """
    Get current authenticated user details.
    This endpoint ONLY reads from cookies, not from Authorization headers.
    """
    return current_user