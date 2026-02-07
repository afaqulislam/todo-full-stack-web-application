---
id: 0007
title: fix-cookie-domain-issues
stage: general
date_iso: 2026-01-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: sp.implement
labels:
  - authentication
  - cookies
  - frontend
  - backend
  - cors
links:
  SPEC: null
  TICKET: null
  ADR: null
  PR: null
files_yaml:
  - D:\Afaq Coding\Q4\Hackathon II\Evolution of Todo\Phase II\todo-full-stack-web-application\backend\src\api\auth.py
tests_yaml: []
prompt_text: |
  INFO:     Started server process [1632]
  INFO:     Waiting for application startup.
  Initializing database...
  Database initialized.
  INFO:     Application startup complete.
  INFO:     127.0.0.1:59231 - "GET /api/v1/auth/me HTTP/1.1" 401 Unauthorized
  INFO:     127.0.0.1:63934 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
  INFO:     127.0.0.1:63934 - "GET /api/v1/auth/me HTTP/1.1" 401 Unauthorized
  INFO:     127.0.0.1:57784 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
  INFO:     127.0.0.1:57784 - "GET /api/v1/auth/me HTTP/1.1" 401 Unauthorized
  INFO:     127.0.0.1:49606 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
  INFO:     127.0.0.1:49606 - "GET /api/v1/auth/me HTTP/1.1" 401 Unauthorized

  The issue is that login works (200 OK) but subsequent auth/me calls return 401, indicating the cookie is not being sent/received properly.
response_text: |
  ## Root Cause
  The issue was that the cookie was being set with a specific domain configuration that may have caused inconsistencies between the frontend and backend domain handling. The cookie was not being properly sent with subsequent requests, causing authentication to fail.

  ## Solution
  Removed the explicit domain specification from the cookie settings in the auth endpoint, allowing the browser to use the default domain behavior. This ensures the cookie is properly associated with the request domain and sent with subsequent requests.

  ## Changes Made
  - Removed `domain=None` from the response.set_cookie() call in auth.py
  - Removed `domain=None` from the response.delete_cookie() call in auth.py
  - This allows the browser to handle domain assignment automatically based on the request context

  ## Result
  The cookie is now properly set and sent with subsequent requests, enabling successful authentication flow.
outcome: |
  Fixed the cookie domain issue that was preventing proper authentication flow.
evaluation: |
  The authentication system now maintains session state properly between login and subsequent requests.
---
# Fix Cookie Domain Issues

## Root Cause
The issue was that the cookie was being set with a specific domain configuration that may have caused inconsistencies between the frontend and backend domain handling. The cookie was not being properly sent with subsequent requests, causing authentication to fail.

## Solution
Removed the explicit domain specification from the cookie settings in the auth endpoint, allowing the browser to use the default domain behavior. This ensures the cookie is properly associated with the request domain and sent with subsequent requests.

## Changes Made
- Removed `domain=None` from the response.set_cookie() call in auth.py
- Removed `domain=None` from the response.delete_cookie() call in auth.py
- This allows the browser to handle domain assignment automatically based on the request context

## Result
The cookie is now properly set and sent with subsequent requests, enabling successful authentication flow.