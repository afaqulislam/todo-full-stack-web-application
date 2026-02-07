from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from datetime import datetime
import enum

if TYPE_CHECKING:
    from .todo import Todo


class UserRole(str, enum.Enum):
    USER = "user"


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)


class User(UserBase, table=True):
    """
    User model representing an authenticated user in the system.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    hashed_password: str
    role: UserRole = Field(default=UserRole.USER)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to todos
    todos: list["Todo"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserRead(UserBase):
    """
    Schema for reading user data (without sensitive information).
    """
    id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserUpdate(SQLModel):
    """
    Schema for updating user information.
    """
    email: Optional[str] = None