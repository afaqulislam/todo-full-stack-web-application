from sqlmodel import select
from typing import Optional
from uuid import UUID
from ..models.user import User, UserCreate, UserRead
from ..core.security import get_password_hash
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    """
    Service layer for User operations.
    """

    @staticmethod
    async def create_user(*, session: AsyncSession, user_create: UserCreate) -> UserRead:
        """
        Create a new user with a hashed password.
        """
        # Check if user already exists
        existing_user_result = await session.execute(select(User).where(User.email == user_create.email))
        existing_user = existing_user_result.scalars().first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash the password
        hashed_password = get_password_hash(user_create.password)

        # Create the user
        db_user = User(
            email=user_create.email,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            hashed_password=hashed_password
        )

        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)

        return UserRead.model_validate(db_user)

    @staticmethod
    async def get_user_by_id(*, session: AsyncSession, user_id: UUID) -> Optional[UserRead]:
        """
        Retrieve a user by ID.
        """
        statement = select(User).where(User.id == user_id)
        result = await session.execute(statement)
        user = result.scalars().first()

        if not user:
            return None

        return UserRead.model_validate(user)

    @staticmethod
    async def get_user_by_email(*, session: AsyncSession, email: str) -> Optional[User]:
        """
        Retrieve a user by email.
        """
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        user = result.scalars().first()

        return user

    @staticmethod
    async def delete_user(*, session: AsyncSession, user_id: UUID) -> bool:
        """
        Delete a user by ID.
        """
        statement = select(User).where(User.id == user_id)
        result = await session.execute(statement)
        user = result.scalars().first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        await session.delete(user)
        await session.commit()

        return True