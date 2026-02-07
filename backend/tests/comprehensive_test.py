import requests
import time

# Server URL
BASE_URL = "http://127.0.0.1:8001"

print("Testing Todo API functionality with cookie-based authentication...")

# Create a session to persist cookies
session = requests.Session()

# Test 1: Health check
print("\n1. Testing health check endpoint...")
try:
    response = session.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code} - {response.json()}")
except Exception as e:
    print(f"Health check failed: {e}")

# Test 2: Root endpoint
print("\n2. Testing root endpoint...")
try:
    response = session.get(f"{BASE_URL}/")
    print(f"Root endpoint: {response.status_code} - {response.json()}")
except Exception as e:
    print(f"Root endpoint failed: {e}")

# Test 3: Registration
print("\n3. Testing user registration...")
registration_data = {
    "email": "test@example.com",
    "password": "testpassword123"
}
try:
    response = session.post(f"{BASE_URL}/api/v1/auth/register", json=registration_data)
    print(f"Registration: {response.status_code}")
    if response.status_code == 201:
        print("User registered successfully")
        user_data = response.json()
        print(f"Created user: {user_data['email']}")
    else:
        print(f"Registration failed: {response.text}")
except Exception as e:
    print(f"Registration failed: {e}")

# Test 4: Login (should set cookie)
print("\n4. Testing user login (cookie-based)...")
login_data = {
    "username": "test@example.com",  # Note: username field is used for email in OAuth2
    "password": "testpassword123"
}
try:
    response = session.post(f"{BASE_URL}/api/v1/auth/login", data=login_data)
    print(f"Login: {response.status_code}")
    if response.status_code == 200:
        print("User logged in successfully")

        # Check if cookie was set
        cookies = session.cookies.get_dict()
        print(f"Cookies after login: {list(cookies.keys())}")

        if 'access_token' in cookies:
            print("✓ Access token cookie set successfully")

            # Test 5: Get current user with cookie
            print("\n5. Testing /auth/me endpoint with valid cookie...")
            try:
                response = session.get(f"{BASE_URL}/api/v1/auth/me")
                print(f"Get current user: {response.status_code}")
                if response.status_code == 200:
                    user_info = response.json()
                    print(f"Current user retrieved: {user_info['email']}")
                else:
                    print(f"Failed to get current user: {response.text}")
            except Exception as e:
                print(f"Get current user failed: {e}")

            # Test 6: Create a todo
            print("\n6. Testing todo creation with cookie...")
            todo_data = {
                "title": "Test Todo",
                "description": "This is a test todo item"
            }
            try:
                response = session.post(f"{BASE_URL}/api/v1/todos/", json=todo_data)
                print(f"Create todo: {response.status_code}")
                if response.status_code == 201:
                    todo = response.json()
                    print(f"Todo created: {todo['title']}")
                    todo_id = todo['id']

                    # Test 7: Get the created todo
                    print("\n7. Testing getting specific todo...")
                    try:
                        response = session.get(f"{BASE_URL}/api/v1/todos/{todo_id}")
                        print(f"Get todo: {response.status_code}")
                        if response.status_code == 200:
                            retrieved_todo = response.json()
                            print(f"Retrieved todo: {retrieved_todo['title']}")
                        else:
                            print(f"Failed to get todo: {response.text}")
                    except Exception as e:
                        print(f"Get todo failed: {e}")

                    # Test 8: Get all todos
                    print("\n8. Testing getting all todos...")
                    try:
                        response = session.get(f"{BASE_URL}/api/v1/todos/")
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

            # Test 9: Logout
            print("\n9. Testing logout...")
            try:
                response = session.post(f"{BASE_URL}/api/v1/auth/logout")
                print(f"Logout: {response.status_code}")
                if response.status_code == 200:
                    print("Logout successful")

                    # Verify that cookie is cleared
                    cookies_after_logout = session.cookies.get_dict()
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

# Test 10: Test unauthorized access after logout
print("\n10. Testing unauthorized access (without valid cookie)...")
try:
    response = session.get(f"{BASE_URL}/api/v1/auth/me")
    print(f"Unauthorized access attempt: {response.status_code}")
    if response.status_code == 401:
        print("Properly rejected unauthorized request")
    else:
        print(f"Unexpected response for unauthorized access: {response.text}")
except Exception as e:
    print(f"Unauthorized access test failed: {e}")

print("\nAPI tests completed!")