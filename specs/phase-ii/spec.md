# Feature Specification: Phase II – Todo Full-Stack Web Application

**Feature Branch**: `002-phase-ii-todo-app`
**Created**: 2026-01-09
**Status**: Final
**Input**: Complete specification for a production-grade full-stack Todo application with authentication, authorization, and user data isolation.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Secure Task Management (Priority: P1)

As a registered user, I want to manage my personal list of tasks securely so that only I can see and modify them.

**Why this priority**: This is the core functionality of the application - without secure, isolated task management, the app fails to meet basic requirements.

**Independent Test**: Can be fully tested by creating tasks for one user and verifying that another user cannot access them, delivering the fundamental value proposition of a secure todo app.

**Acceptance Scenarios**:

1. **Given** a user is logged in, **When** they create a task, **Then** the task MUST be saved to their specific user ID in the database.
2. **Given** a user is logged in, **When** they fetch their tasks, **Then** they MUST ONLY see tasks where the `user_id` matches their own.
3. **Given** User A's task ID, **When** User B attempts to edit/delete it via API, **Then** the backend MUST return a 403 Forbidden or 404 Not Found error.
4. **Given** a user creates a task, **When** they log out and log in from another device, **Then** they MUST be able to see their tasks again.

---

### User Story 2 - Real-time Authentication & Persistence (Priority: P1)

As a user, I want my session to remain valid across page refreshes and my data to persist across devices.

**Why this priority**: Essential for user experience - users need to maintain their session and have their data available consistently.

**Independent Test**: Can be tested by logging in, refreshing the page, and verifying the session remains active, delivering seamless user experience.

**Acceptance Scenarios**:

1. **Given** a user logs in via Better Auth, **When** the frontend makes an API call, **Then** it MUST attach a valid JWT to the Authorization header.
2. **Given** the backend receives a request, **When** the JWT is invalid or missing, **Then** it MUST return a 401 Unauthorized error.
3. **Given** a user's session expires, **When** they make an API call, **Then** they MUST be redirected to the login page.

---

### User Story 3 - Task Operations (Priority: P2)

As a user, I want to create, read, update, and delete my tasks with status toggling functionality.

**Why this priority**: These are the essential CRUD operations that make the todo app functional beyond just secure storage.

**Independent Test**: Can be tested by performing all CRUD operations on tasks, delivering complete task management functionality.

**Acceptance Scenarios**:

1. **Given** a user is authenticated, **When** they create a task, **Then** it MUST appear in their task list with a unique ID and correct ownership.
2. **Given** a user has tasks, **When** they mark a task as complete, **Then** the task status MUST update in the database and reflect in the UI.
3. **Given** a user wants to delete a task, **When** they click delete, **Then** the task MUST be removed from their list only.

---

### Edge Cases

- What happens when a user tries to access a task ID that doesn't exist? The system MUST return 404 Not Found.
- How does the system handle expired JWT tokens? The system MUST return 401 Unauthorized and redirect to login.
- What happens when a user tries to access another user's data? The system MUST return 403 Forbidden or 404 Not Found to prevent enumeration.
- How does the system handle concurrent modifications? The system MUST handle them safely without data corruption.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: User registration and login via Better Auth (Frontend).
- **FR-002**: CRUD operations for Todos (Create, Read, Update, Delete).
- **FR-003**: Todo status toggling (Complete/Incomplete).
- **FR-004**: JWT issuance on frontend and verification on backend.
- **FR-005**: Database persistence using SQLModel and Neon PostgreSQL.
- **FR-006**: User data isolation - each user can only access their own data.
- **FR-007**: Session persistence across page refreshes using JWT tokens.
- **FR-008**: Proper error handling with appropriate HTTP status codes.

### Non-Functional Requirements

- **NFR-001**: **Security**: No endpoint shall allow unauthorized or cross-user access.
- **NFR-002**: **Performance**: P95 backend response time < 100ms for CRUD operations.
- **NFR-003**: **Reliability**: 99.9% uptime for API services.
- **NFR-004**: **Scalability**: Stateless backend design to support horizontal scaling.
- **NFR-005**: **Availability**: API endpoints must be accessible 99.9% of the time.
- **NFR-006**: **Maintainability**: Code must follow clean architecture principles with clear separation of concerns.

### Key Entities

- **User**: Represents an authenticated user with unique ID, email, and authentication data managed by Better Auth.
- **Todo**: Represents a task with ID, title, description, completion status, creation timestamp, and user_id for ownership.
- **Session**: Represents an active user session with JWT token for backend authentication.

## Authentication & Authorization Rules

- **Better Auth**: Handles user identity, OAuth providers, and session management on the frontend.
- **JWT Verification**: The frontend will extract a JWT (or exchange a session cookie for one) to communicate with the backend.
- **Permission Level**: All users have equal "User" permissions, but visibility is limited to owned resources (`owner_id` or `user_id` match).
- **Cross-User Access Prevention**: Any attempt to access another user's data MUST result in 403 Forbidden or 404 Not Found.
- **Session Validation**: All API requests MUST include a valid JWT in the Authorization header.

## JWT Flow: Next.js ↔ FastAPI

1. **Frontend**: User authenticates with Better Auth in the Next.js app.
2. **Token Acquisition**: The frontend retrieves the JWT (Access Token).
3. **API Request**: Frontend sends `GET /api/v1/todos` with `Authorization: Bearer <JWT>`.
4. **Backend Verification**: FastAPI middleware intercepts the request:
   - Decodes JWT using the shared symmetric secret or public key.
   - Validates `exp` (expiration), `iss` (issuer), and `sub` (subject/user_id).
5. **Context Injection**: The `user_id` is injected into the request state for use by service logic.
6. **Request Processing**: The backend processes the request with user context, enforcing ownership checks.

## API Behavior Rules

- **Base URL**: `/api/v1`
- **Response Format**: Always JSON.
- **Success Codes**: 200 OK (Read/Update), 201 Created (Create), 204 No Content (Delete).
- **Versioning**: Mandatory prefixing with `/v1`.
- **Request Format**: JSON for all request bodies.
- **Rate Limiting**: API endpoints should implement rate limiting to prevent abuse.

## User Data Isolation Rules

- **Database Constraint**: Every table containing user-specific data MUST have a `user_id` column.
- **Policy Enforcement**: Every service-layer function MUST require a `user_id` argument and include it in the `WHERE` clause of every SQL query.
- **Ownership Validation**: Before any data modification, verify that the requesting user owns the resource.
- **Cross-User Prevention**: Any query results MUST be filtered to only include data owned by the authenticated user.

## Error Handling Rules

- **Format**: `{"error": "string_code", "message": "human_readable_detail"}`.
- **401 Unauthorized**: Missing or invalid JWT.
- **403 Forbidden**: Found record exists but belongs to another user.
- **404 Not Found**: Record does not exist (preferred over 403 to prevent ID enumeration).
- **422 Unprocessable Entity**: Validation failure (Pydantic).
- **500 Internal Server Error**: Unexpected server errors with minimal detail to prevent information disclosure.

## Environment Variables Required

### Backend (.env)
- `DATABASE_URL`: Neon PostgreSQL connection string.
- `JWT_SECRET`: Secret key for token verification.
- `JWT_ALGORITHM`: e.g., "HS256".
- `API_HOST`: Host for the backend server.
- `API_PORT`: Port for the backend server.

### Frontend (.env.local)
- `BETTER_AUTH_SECRET`: Secret for Better Auth encryption.
- `NEXT_PUBLIC_API_URL`: Backend API URL.
- `DATABASE_URL`: Connection string for Better Auth session management.
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Public URL for Better Auth endpoints.

## Out-of-Scope Items

- Task sharing or collaboration features.
- Multi-tenancy (beyond user isolation).
- Offline synchronization (Phase III candidate).
- File attachments to Todos.
- Advanced search and filtering capabilities.
- Task categorization or tagging.
- Recurring tasks functionality.
- Email notifications for tasks.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of API endpoints protected by JWT.
- **SC-002**: 0% incidence of cross-user data leakage during automated security tests.
- **SC-003**: Backend tests cover 100% of the User Data Isolation logic.
- **SC-004**: Users can perform all CRUD operations on their tasks with <100ms response time (P95).
- **SC-005**: 99.9% of API requests return successful responses under normal operating conditions.
- **SC-006**: All authentication and authorization checks are validated through automated tests.