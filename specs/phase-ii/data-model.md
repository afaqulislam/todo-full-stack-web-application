# Data Model: Phase II – Todo Full-Stack Web Application

**Date**: 2026-01-09
**Feature**: Phase II Todo Application
**Data Model**: SQLModel-based entities

## Entity Relationships

```
User (1) -----> (Many) Todo
```

## User Entity

### Table: `users`
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the user |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address |
| hashed_password | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

### SQLModel Definition
```python
class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(sa_column=Column(String, unique=True, index=True))
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to todos
    todos: List["Todo"] = Relationship(back_populates="user")
```

## Todo Entity

### Table: `todos`
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the todo |
| title | VARCHAR(255) | NOT NULL | Title of the todo item |
| description | TEXT | NULL | Optional description of the todo |
| completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| user_id | UUID | FOREIGN KEY, NOT NULL | Owner of this todo |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

### SQLModel Definition
```python
class Todo(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(sa_column=Column(String, index=True))
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    user_id: UUID = Field(foreign_key="users.id", ondelete="CASCADE")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: User = Relationship(back_populates="todos")
```

## Database Constraints

### Primary Keys
- All entities use UUID primary keys for global uniqueness
- Auto-generated using `uuid4()` function

### Foreign Keys
- `todos.user_id` references `users.id`
- ON DELETE CASCADE to automatically remove todos when user is deleted
- Ensures referential integrity

### Indexes
- `users.email`: Unique index for fast user lookup
- `todos.user_id`: Index for efficient user-based queries
- `todos.title`: Index for search functionality (future enhancement)
- `todos.completed`: Index for filtering by completion status

## Data Validation Rules

### User Validation
- Email format validation using Pydantic
- Password strength requirements (handled by Better Auth)
- Unique email constraint enforced at database level

### Todo Validation
- Title length: 1-255 characters
- User ID must reference existing user
- Completion status defaults to false
- Automatic timestamp management

## Security Considerations

### Data Isolation
- All queries must filter by `user_id` to prevent cross-user access
- No direct access to other users' data is possible
- Foreign key constraints prevent orphaned records

### Access Patterns
- Always query todos with `WHERE user_id = :current_user_id`
- Never expose user_id in client-side responses for other users
- Use JOIN operations carefully to maintain isolation

## Migration Strategy

### Initial Schema
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_completed ON todos(completed);
```

### Future Extensions
- Add soft delete capability with `deleted_at` field
- Add categories or tags with separate tables
- Add due dates and reminders functionality
- Add sharing capabilities (in future phases)

## Performance Considerations

### Query Optimization
- Use indexes for frequently queried fields
- Implement pagination for large result sets
- Consider read replicas for high-read scenarios
- Use connection pooling for database operations

### Scalability
- UUID primary keys support horizontal sharding
- Proper indexing supports efficient queries
- Foreign key constraints maintain data integrity
- Consider partitioning for very large datasets