# Todo Full-Stack Web Application

![Python](https://img.shields.io/badge/python-3.9+-blue.svg) ![FastAPI](https://img.shields.io/badge/fastapi-0.104.1-green.svg) ![Next.js](https://img.shields.io/badge/next.js-16.1.3-black.svg) ![PostgreSQL](https://img.shields.io/badge/postgresql-DB-blue.svg) ![TailwindCSS](https://img.shields.io/badge/tailwindcss-v4.1.18-38bdf8.svg)

## 📋 Project Overview

This is a production-grade full-stack web application for managing todos with user authentication and authorization. The application consists of a FastAPI backend with PostgreSQL database and a Next.js frontend with Tailwind CSS styling. It provides a complete solution for users to register, authenticate, and manage their personal todo lists with secure JWT-based authentication.

The system solves the common problem of task management with proper user isolation, ensuring that users can only access and modify their own todos. It implements industry-standard security practices and follows modern web development patterns.

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (0.104.1)
- **Database**: PostgreSQL (with SQLModel ORM)
- **Authentication**: JWT with bcrypt password hashing
- **Dependencies**: python-jose, passlib, python-dotenv, alembic
- **Runtime**: Python 3.9+

### Frontend
- **Framework**: Next.js 16.1.3 (App Router)
- **Styling**: Tailwind CSS v4.1.18
- **Runtime**: React 19.2.3
- **State Management**: React Context API

### Infrastructure & Tooling
- **Database Migration**: Alembic
- **Async Database Drivers**: asyncpg, psycopg2-binary
- **Development**: TypeScript, ESLint, PostCSS
- **Security**: JWT, bcrypt, python-jose

## 🏗️ Architecture Overview

The application follows a microservices-like architecture with a clear separation between frontend and backend:

- **Frontend Layer**: Next.js application serving the user interface and handling client-side state management
- **API Layer**: FastAPI backend providing RESTful endpoints with authentication and authorization
- **Data Layer**: PostgreSQL database with SQLModel ORM for data persistence
- **Authentication Layer**: JWT-based authentication system with secure token management

The frontend communicates with the backend through REST API calls, with authentication handled via JWT tokens stored in cookies. The backend enforces user ownership rules, ensuring users can only access their own data.

## 📁 Project Structure

```
todo-full-stack-web-application/
├── backend/
│   ├── src/
│   │   ├── api/           # API route definitions (auth, todos)
│   │   ├── core/          # Core configurations and database setup
│   │   ├── models/        # Database models
│   │   ├── services/      # Business logic services
│   │   └── main.py        # Application entry point
│   ├── tests/             # Backend test suite
│   ├── requirements.txt   # Python dependencies
│   └── README.md          # Backend documentation
├── frontend/
│   ├── app/               # Next.js app router pages
│   ├── components/        # Reusable UI components
│   ├── public/            # Static assets
│   ├── middleware.ts      # Route protection middleware
│   ├── package.json       # Node.js dependencies
│   └── README.md          # Frontend documentation
├── specs/                 # Project specifications
├── history/               # Development history
└── README.md              # This file
```

## ⚙️ Environment Configuration

### Backend Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
# DATABASE (PostgreSQL)
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db

# AUTHENTICATION (JWT)
BETTER_AUTH_SECRET=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRY_DAYS=7
ACCESS_TOKEN_EXPIRE_MINUTES=30

# APPLICATION
ENV=development
API_PORT=8000
API_DOCS_ENABLED=true
BACKEND_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Environment Variable Details

- `DATABASE_URL`: PostgreSQL connection string (Neon DB recommended for cloud deployment)
- `BETTER_AUTH_SECRET`: Secret key for JWT signing (use a strong random key in production)
- `JWT_ALGORITHM`: Algorithm used for JWT signing (HS256 recommended)
- `JWT_EXPIRY_DAYS`: Number of days until JWT tokens expire
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Minutes until access tokens expire
- `ENV`: Environment mode (development/production)
- `API_PORT`: Port to run the API server on
- `API_DOCS_ENABLED`: Whether to enable API documentation endpoints
- `BACKEND_CORS_ORIGINS`: Comma-separated list of allowed origins for CORS

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 18+ with npm
- PostgreSQL database (local or cloud-based)

### Backend Setup

1. **Navigate to the backend directory**
```bash
cd backend
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables** (see above)

5. **Start the backend server**
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Navigate to the frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start the development server**
```bash
npm run dev
```

4. **Open the application**
Visit `http://localhost:3000` in your browser

## 🔄 Runtime Behavior

### Application Flow
1. **Startup**: Backend initializes database connection and creates tables if needed
2. **Authentication**: Users register/login to obtain JWT tokens
3. **Data Access**: Frontend makes authenticated API calls to backend
4. **Authorization**: Backend verifies tokens and enforces user ownership
5. **Response**: Backend returns data, frontend renders UI

### Data Flow
- User interacts with Next.js frontend
- Frontend makes API calls to FastAPI backend
- Backend validates JWT tokens and authorizes requests
- Backend queries PostgreSQL database
- Backend returns JSON responses to frontend
- Frontend updates UI based on responses

### State Management
- Frontend uses React Context API for authentication state
- Backend maintains user session through JWT tokens
- Database stores persistent todo data with user relationships

## ⚠️ Error Handling & Common Failures

### Potential Failures
- **Database Connection Issues**: Invalid `DATABASE_URL` or database server down
- **Authentication Failures**: Invalid credentials or expired tokens
- **Authorization Errors**: Attempting to access unauthorized resources
- **Network Issues**: Connectivity problems between frontend and backend

### Identification & Recovery
- **Database Issues**: Check logs for connection errors, verify `DATABASE_URL`
- **Auth Problems**: Clear browser cookies, re-register/login
- **API Errors**: Check backend logs, verify token validity
- **CORS Issues**: Ensure `BACKEND_CORS_ORIGINS` includes frontend URL

### Health Checks
- Backend health: `GET /health` returns application status
- Frontend connectivity: Verify API endpoints are accessible

## 🛠️ Build & Deployment Notes

### Frontend Build Process
```bash
npm run build
npm start
```

### Backend Production Deployment
```bash
uvicorn src.main:app --host 0.0.0.0 --port $API_PORT --workers 4
```

### Production Considerations
- Use HTTPS in production environments
- Implement proper logging and monitoring
- Set up database backups and maintenance
- Configure reverse proxy (nginx) for production
- Use environment-specific configurations
- Implement rate limiting for API endpoints

## 🔐 Security & Constraints

### Implemented Security Measures
- **Password Hashing**: bcrypt for secure password storage
- **JWT Authentication**: Signed tokens with configurable expiry
- **Input Validation**: Pydantic models enforce data validation
- **CORS Configuration**: Restricted origins in production
- **User Isolation**: Users can only access their own data
- **SQL Injection Prevention**: ORM handles query parameterization

### System Limitations
- Single database instance (no horizontal scaling)
- Cookie-based authentication limits cross-origin usage
- No refresh token mechanism implemented
- Rate limiting not configured by default

## 📡 API Endpoints

### Authentication (`/api/v1/auth`)
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login with email and password
- `GET /api/v1/auth/me` - Get current user details

### Todos (`/api/v1/todos`)
- `POST /api/v1/todos/` - Create a new todo
- `GET /api/v1/todos/{todo_id}` - Get a specific todo
- `GET /api/v1/todos/` - Get all todos for current user
- `PUT /api/v1/todos/{todo_id}` - Update a specific todo
- `PATCH /api/v1/todos/{todo_id}` - Partially update a todo
- `DELETE /api/v1/todos/{todo_id}` - Delete a specific todo
- `POST /api/v1/todos/{todo_id}/toggle` - Toggle todo completion status

### System Endpoints
- `GET /` - Root endpoint for health check
- `GET /health` - Health check endpoint

## 🏥 Health Check

The application provides a health check endpoint at `/health` which returns:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

## 📚 API Documentation

The backend provides interactive API documentation through:
- **Swagger UI**: Available at `http://localhost:8000/api/v1/docs`
- **ReDoc**: Available at `http://localhost:8000/api/v1/redoc`

Documentation is auto-generated from the FastAPI application and includes request/response schemas, example payloads, and authentication requirements.

## 🧪 Testing

### Backend Tests
Run backend tests using pytest:
```bash
cd backend
pytest tests/
```

### Frontend Tests
Run frontend tests (if available):
```bash
cd frontend
npm test
```

### Manual Testing
1. Register a new user via `/api/v1/auth/register`
2. Login via `/api/v1/auth/login` to obtain a JWT token
3. Test protected endpoints with the token in Authorization header
4. Verify user isolation by testing cross-user access attempts

## 🤝 Contributing Guidelines

We welcome contributions to this project! To contribute:

1. Fork the repository and create your branch from `main`
2. Follow the established code style and patterns
3. Write tests for new functionality
4. Ensure all tests pass before submitting a pull request
5. Document any changes to the API or functionality
6. Submit a pull request with a clear description of your changes

Please ensure your code adheres to the project's coding standards and includes appropriate unit tests.

## 👨‍💻 Maintainer / Author Information

**Afaq Ul Islam**  
Frontend / Full-Stack Web Developer  
AI, Web3 & Agentic AI Learner (GIAIC)

This project is designed, developed, and maintained by **Afaq Ul Islam**.  
All architectural decisions, implementation details, and maintenance responsibilities belong to the author unless explicitly stated otherwise.

---

## 🛟 Support & Maintenance

This project is currently **self-maintained**.

Support is handled as follows:
- Bugs and issues should be reported via the GitHub Issues section
- Improvements and enhancements can be proposed through Pull Requests
- Code reviews are performed by the maintainer
- Dependency updates and fixes are applied as needed

There is **no guaranteed SLA**, enterprise support contract, or dedicated support team.

---

## 📄 License

This project is released under the **MIT License**.

You are free to use, modify, and distribute this project in accordance with the terms of the license.  
See the `LICENSE` file in the repository root for full details.

---

## 🌐 Social / Contact

**Afaq Ul Islam**

- **GitHub**: https://github.com/afaqulislam  
- **LinkedIn**: https://linkedin.com/in/afaqulislam
- **Twitter(X)**: https://x.com/afaqulislam708 
- **Email**: afaqulislam707@gmail.com  

For professional collaboration, technical discussions, or project-related communication, email is the preferred contact method.
