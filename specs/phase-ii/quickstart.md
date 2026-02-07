# Quickstart Guide: Phase II – Todo Full-Stack Web Application

**Date**: 2026-01-09
**Feature**: Phase II Todo Application
**Version**: 1.0

## Prerequisites

### System Requirements
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)
- PostgreSQL-compatible database (Neon recommended)
- Git version control
- Package managers: pip and npm/yarn

### Environment Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Navigate to the project root directory

## Backend Setup

### 1. Create Virtual Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
JWT_SECRET=your-super-secret-jwt-key-here
JWT_ALGORITHM=HS256
API_HOST=0.0.0.0
API_PORT=8000
```

### 4. Database Initialization
```bash
# Run database migrations
python -m src.main migrate

# Or initialize the database directly
python -c "from src.core.database import create_db_and_tables; create_db_and_tables()"
```

### 5. Start Backend Server
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend will be available at: `http://localhost:8000`

## Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Environment Configuration
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-better-auth-secret-here
DATABASE_URL=postgresql://username:password@localhost:5432/better_auth
```

### 4. Start Frontend Development Server
```bash
npm run dev
# or
yarn dev
```

Frontend will be available at: `http://localhost:3000`

## Development Workflow

### Running Both Servers Simultaneously
Use a process manager like `concurrently`:
```bash
# From project root
npm install -g concurrently
concurrently "cd backend && uvicorn src.main:app --reload" "cd frontend && npm run dev"
```

### API Documentation
Backend API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

### Backend Tests
```bash
# Run all backend tests
cd backend
pytest

# Run tests with coverage
pytest --cov=src

# Run specific test file
pytest tests/unit/test_todo_service.py
```

### Frontend Tests
```bash
# Run all frontend tests
cd frontend
npm test

# Run tests in watch mode
npm test -- --watch
```

## Database Migrations

### Creating New Migrations
```bash
# Backend directory
cd backend

# Using alembic for migrations (if configured)
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head
```

## Production Deployment

### Backend Build
```bash
cd backend
pip install -r requirements.txt
# Use a WSGI/ASGI server like gunicorn
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend Build
```bash
cd frontend
npm run build
npm start  # or serve using your preferred static server
```

## Common Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start frontend development server |
| `uvicorn src.main:app --reload` | Start backend development server |
| `pytest` | Run backend tests |
| `npm test` | Run frontend tests |
| `npm run build` | Build frontend for production |
| `python -c "..."` | Execute Python one-liners |

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   - Change ports in `.env` files
   - Kill existing processes using the port

2. **Database Connection Issues**
   - Verify DATABASE_URL is correct
   - Ensure PostgreSQL server is running
   - Check firewall settings

3. **Authentication Issues**
   - Verify JWT_SECRET matches between frontend and backend
   - Ensure Better Auth is properly configured

4. **CORS Errors**
   - Check backend CORS settings
   - Verify frontend origin is allowed

### Environment Variables Reference

**Backend (.env):**
- `DATABASE_URL`: Database connection string
- `JWT_SECRET`: Secret key for JWT signing
- `JWT_ALGORITHM`: Algorithm for JWT (default: HS256)
- `API_HOST`: Host for the API server
- `API_PORT`: Port for the API server

**Frontend (.env.local):**
- `NEXT_PUBLIC_API_URL`: Base URL for backend API
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Better Auth server URL
- `BETTER_AUTH_SECRET`: Better Auth secret key
- `DATABASE_URL`: Better Auth database connection

## Next Steps

1. Review the [implementation plan](./plan.md) for detailed development steps
2. Examine the [data model](./data-model.md) for entity relationships
3. Check the [research document](./research.md) for technical decisions
4. Begin with the [tasks](../tasks.md) for implementation