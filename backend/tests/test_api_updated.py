#!/usr/bin/env python3
"""
Test script to verify the Todo API authentication and functionality with cookie-based auth.
"""
import asyncio
import httpx
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

async def test_api():
    print("Testing Todo API functionality with cookie-based authentication...")

    # Create an async HTTP client with cookie persistence
    async with httpx.AsyncClient(base_url=BASE_URL, follow_redirects=True) as client:

        # Test 1: Health check
        print("\n1. Testing health check endpoint...")
        try:
            response = await client.get("/health")
            print(f"Health check: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"Health check failed: {e}")

        # Test 2: Registration
        print("\n2. Testing user registration...")
        registration_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        try:
            response = await client.post("/api/v1/auth/register", json=registration_data)
            print(f"Registration: {response.status_code}")
            if response.status_code == 201:
                print("User registered successfully")
                user_data = response.json()
                print(f"Created user: {user_data['email']}")
            else:
                print(f"Registration failed: {response.text}")
        except Exception as e:
            print(f"Registration failed: {e}")

        # Test 3: Login (should set cookie)
        print("\n3. Testing user login (cookie-based)...")
        login_data = {
            "username": "test@example.com",  # Note: username field is used for email in OAuth2
            "password": "testpassword123"
        }
        try:
            response = await client.post("/api/v1/auth/login", data=login_data)
            print(f"Login: {response.status_code}")
            if response.status_code == 200:
                print("User logged in successfully")

                # Check if cookie was set
                cookies = dict(client.cookies)
                print(f"Cookies after login: {list(cookies.keys())}")

                if 'access_token' in cookies:
                    print("✓ Access token cookie set successfully")

                    # Test 4: Get current user with cookie
                    print("\n4. Testing /auth/me endpoint with valid cookie...")
                    try:
                        response = await client.get("/api/v1/auth/me")
                        print(f"Get current user: {response.status_code}")
                        if response.status_code == 200:
                            user_info = response.json()
                            print(f"Current user retrieved: {user_info['email']}")
                        else:
                            print(f"Failed to get current user: {response.text}")
                    except Exception as e:
                        print(f"Get current user failed: {e}")

                    # Test 5: Create a todo
                    print("\n5. Testing todo creation with cookie...")
                    todo_data = {
                        "title": "Test Todo",
                        "description": "This is a test todo item"
                    }
                    try:
                        response = await client.post("/api/v1/todos/", json=todo_data)
                        print(f"Create todo: {response.status_code}")
                        if response.status_code == 201:
                            todo = response.json()
                            print(f"Todo created: {todo['title']}")
                            todo_id = todo['id']

                            # Test 6: Get the created todo
                            print("\n6. Testing getting specific todo...")
                            try:
                                response = await client.get(f"/api/v1/todos/{todo_id}")
                                print(f"Get todo: {response.status_code}")
                                if response.status_code == 200:
                                    retrieved_todo = response.json()
                                    print(f"Retrieved todo: {retrieved_todo['title']}")
                                else:
                                    print(f"Failed to get todo: {response.text}")
                            except Exception as e:
                                print(f"Get todo failed: {e}")

                            # Test 7: Get all todos
                            print("\n7. Testing getting all todos...")
                            try:
                                response = await client.get("/api/v1/todos/")
                                print(f"Get all todos: {response.status_code}")
                                if response.status_code == 200:
                                    todos = response.json()
                                    print(f"Retrieved {len(todos)} todos")
                                else:
                                    print(f"Failed to get todos: {response.text}")
                            except Exception as e:
                                print(f"Get all todos failed: {e}")

                        else:
                            print(f"Failed to create todo: {response.text}")
                    except Exception as e:
                        print(f"Create todo failed: {e}")

                    # Test 8: Logout
                    print("\n8. Testing logout...")
                    try:
                        response = await client.post("/api/v1/auth/logout")
                        print(f"Logout: {response.status_code}")
                        if response.status_code == 200:
                            print("Logout successful")

                            # Verify that cookie is cleared
                            cookies_after_logout = dict(client.cookies)
                            print(f"Cookies after logout: {list(cookies_after_logout.keys())}")
                        else:
                            print(f"Logout failed: {response.text}")
                    except Exception as e:
                        print(f"Logout failed: {e}")

                else:
                    print("✗ Access token cookie was not set!")
            else:
                print(f"Login failed: {response.text}")
        except Exception as e:
            print(f"Login failed: {e}")

        # Test 9: Test unauthorized access after logout
        print("\n9. Testing unauthorized access (without valid cookie)...")
        try:
            response = await client.get("/api/v1/auth/me")
            print(f"Unauthorized access attempt: {response.status_code}")
            if response.status_code == 401:
                print("Properly rejected unauthorized request")
            else:
                print(f"Unexpected response for unauthorized access: {response.text}")
        except Exception as e:
            print(f"Unauthorized access test failed: {e}")

if __name__ == "__main__":
    print("Starting API tests...")
    asyncio.run(test_api())
    print("\nAPI tests completed!")