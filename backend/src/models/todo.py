from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from datetime import datetime
import enum

if TYPE_CHECKING:
    from .user import User


class TodoPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TodoStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"


class TodoBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: TodoPriority = Field(default=TodoPriority.MEDIUM)
    status: TodoStatus = Field(default=TodoStatus.TODO)


class Todo(TodoBase, table=True):
    """
    Todo model representing a task item owned by a user.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    priority: TodoPriority = Field(default=TodoPriority.MEDIUM)
    status: TodoStatus = Field(default=TodoStatus.TODO)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: "User" = Relationship(back_populates="todos")


class TodoCreate(TodoBase):
    """
    Schema for creating a new todo item.
    """
    title: str
    status: Optional[TodoStatus] = None


class TodoRead(TodoBase):
    """
    Schema for reading todo data.
    """
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class TodoUpdate(SQLModel):
    """
    Schema for updating todo information.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[TodoPriority] = None
    status: Optional[TodoStatus] = None


class TodoPatch(SQLModel):
    """
    Schema for partial updates to todo information.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[TodoPriority] = None
    status: Optional[TodoStatus] = None