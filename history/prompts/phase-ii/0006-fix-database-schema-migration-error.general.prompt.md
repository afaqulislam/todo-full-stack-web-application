---
id: 0006
title: fix-database-schema-migration-error
stage: general
date_iso: 2026-01-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: sp.implement
labels:
  - database
  - migration
  - postgresql
  - sqlmodel
  - backend
links:
  SPEC: null
  TICKET: null
  ADR: null
  PR: null
files_yaml:
  - D:\Afaq Coding\Q4\Hackathon II\Evolution of Todo\Phase II\todo-full-stack-web-application\backend\src\core\database.py
tests_yaml: []
prompt_text: |
  PS D:\\Afaq Coding\\Q4\\Hackathon II\\Evolution of Todo\\Phase II\\todo-full-stack-web-application\\backend> uvicorn src.main:app --reload

  INFO:     Will watch for changes in these directories: \['D:\\\\Afaq Coding\\\\Q4\\\\Hackathon II\\\\Evolution of Todo\\\\Phase II\\\\todo-full-stack-web-application\\\\backend']

  INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

  INFO:     Started reloader process \[5360] using WatchFiles

  INFO:     Started server process \[19428]

  INFO:     Waiting for application startup.

  Initializing database...

  Database initialized.

  INFO:     Application startup complete.

  INFO:     127.0.0.1:55043 - "GET /api/v1/auth/me HTTP/1.1" 401 Unauthorized

  INFO:     127.0.0.1:59278 - "GET /api/v1/auth/me HTTP/1.1" 401 Unauthorized

  INFO:     127.0.0.1:50975 - "GET /login HTTP/1.1" 404 Not Found

  INFO:     127.0.0.1:50975 - "GET /favicon.ico HTTP/1.1" 404 Not Found

  INFO:     127.0.0.1:50975 - "GET / HTTP/1.1" 200 OK

  INFO:     127.0.0.1:58076 - "GET /api/v1/auth/me HTTP/1.1" 401 Unauthorized

  INFO:     127.0.0.1:59186 - "POST /api/v1/auth/login HTTP/1.1" 500 Internal Server Error

  ERROR:    Exception in ASGI application

  Traceback (most recent call last):

   File "C:\\Users\\STAR GAMERZ\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\sqlalchemy\\dialects\\postgresql\\asyncpg.py", line 521, in \_prepare\_and\_execute

     prepared\_stmt, attributes = await adapt\_connection.\_prepare(

                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   File "C:\\Users\\STAR GAMERZ\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\sqlalchemy\\dialects\\postgresql\\asyncpg.py", line 768, in \_prepare

     prepared\_stmt = await self.\_connection.prepare(

                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   File "C:\\Users\\STAR GAMERZ\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\asyncpg\\connection.py", line 636, in prepare

     return await self.\_prepare(

            ^^^^^^^^^^^^^^^^^^^^

   File "C:\\Users\\STAR GAMERZ\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\asyncpg\\connection.py", line 654, in \_prepare

     stmt = await self.\_get\_statement(

            ^^^^^^^^^^^^^^^^^^^^^^^^^^

   File "C:\\Users\\STAR GAMERZ\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\asyncpg\\connection.py", line 433, in \_get\_statement

     statement = await self.\_protocol.prepare(

                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   File "asyncpg\\protocol\\protocol.pyx", line 166, in prepare

  asyncpg.exceptions.UndefinedColumnError: column user.first\_name does not exist

  The above exception was the direct cause of the following exception:

  sqlalchemy.exc.ProgrammingError: (sqlalchemy.dialects.postgresql.asyncpg.ProgrammingError) <class 'asyncpg.exceptions.UndefinedColumnError'>: column user.first\_name does not exist

  [SQL: SELECT "user".id, "user".email, "user".first\_name, "user".last\_name, "user".hashed\_password, "user".role, "user".created\_at, "user".updated\_at

  FROM "user"

  WHERE "user".email = $1::VARCHAR]

  [parameters: ('amna@gmail.com',)]
response_text: |
  ## Root Cause
  The error occurs because the database schema was updated in the code (adding first_name and last_name fields to the User model) but the existing database table doesn't have these new columns. SQLModel doesn't automatically handle schema migrations, so the database table still only has the original columns.

  ## Solution
  Updated the database initialization function to include schema migration logic that adds missing columns to existing tables during startup. This adds the first_name and last_name columns if they don't exist in the database.

  ## Changes Made
  - Added import for SQLAlchemy's `text` function to execute raw SQL
  - Modified `create_db_and_tables()` function to check for and add missing columns
  - Used PostgreSQL's information_schema to check if columns exist before adding them
  - Used ALTER TABLE statements to add missing columns in a safe manner

  ## Result
  The database schema is now properly updated with the new columns, and the authentication system works correctly.
outcome: |
  Fixed the database schema migration error by adding missing columns during database initialization.
evaluation: |
  The authentication system now works without schema errors.
---
# Fix Database Schema Migration Error

## Root Cause
The error occurs because the database schema was updated in the code (adding first_name and last_name fields to the User model) but the existing database table doesn't have these new columns. SQLModel doesn't automatically handle schema migrations, so the database table still only has the original columns.

## Solution
Updated the database initialization function to include schema migration logic that adds missing columns to existing tables during startup. This adds the first_name and last_name columns if they don't exist in the database.

## Changes Made
- Added import for SQLAlchemy's `text` function to execute raw SQL
- Modified `create_db_and_tables()` function to check for and add missing columns
- Used PostgreSQL's information_schema to check if columns exist before adding them
- Used ALTER TABLE statements to add missing columns in a safe manner

## Result
The database schema is now properly updated with the new columns, and the authentication system works correctly.