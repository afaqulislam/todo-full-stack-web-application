import requests
import json

# Test the API endpoints
BASE_URL = "http://localhost:8000"

print("Testing Todo API endpoints...")

# 1. Health check
print("\n1. Testing health check:")
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}, Response: {response.json()}")
except Exception as e:
    print(f"Health check failed: {e}")

# 2. Register a new user
print("\n2. Testing user registration:")
try:
    registration_data = {
        "email": "testuser@example.com",
        "password": "securepassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=registration_data)
    print(f"Registration Status: {response.status_code}")
    if response.status_code == 201:
        print("User registered successfully")
    elif response.status_code == 400:
        print("User already exists, continuing with login...")
    else:
        print(f"Registration failed: {response.text}")
except Exception as e:
    print(f"Registration failed: {e}")

# 3. Login to get token
print("\n3. Testing user login:")
try:
    login_data = {
        "username": "testuser@example.com",  # For OAuth2, username is email
        "password": "securepassword123"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", data=login_data)
    print(f"Login Status: {response.status_code}")
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data['access_token']
        print("Login successful, got access token")

        # 4. Test /auth/me endpoint
        print("\n4. Testing /auth/me endpoint:")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
        print(f"Get current user Status: {response.status_code}")
        if response.status_code == 200:
            user_info = response.json()
            print(f"Current user: {user_info['email']}")
        else:
            print(f"Failed to get current user: {response.text}")

        # 5. Test creating a todo (without user_id in request body)
        print("\n5. Testing todo creation:")
        todo_data = {
            "title": "Test Todo Item",
            "description": "This is a test todo created via API"
        }
        response = requests.post(f"{BASE_URL}/api/v1/todos/", json=todo_data, headers=headers)
        print(f"Create todo Status: {response.status_code}")
        if response.status_code == 201:
            todo = response.json()
            print(f"Todo created successfully: {todo['title']}")
            todo_id = todo['id']

            # 6. Test getting the created todo
            print("\n6. Testing getting specific todo:")
            response = requests.get(f"{BASE_URL}/api/v1/todos/{todo_id}", headers=headers)
            print(f"Get specific todo Status: {response.status_code}")
            if response.status_code == 200:
                retrieved_todo = response.json()
                print(f"Retrieved todo: {retrieved_todo['title']}")
            else:
                print(f"Failed to get specific todo: {response.text}")
        else:
            print(f"Failed to create todo: {response.text}")

        # 7. Test unauthorized access (without token)
        print("\n7. Testing unauthorized access:")
        response = requests.get(f"{BASE_URL}/api/v1/auth/me")
        print(f"Unauthorized access Status: {response.status_code}")
        if response.status_code == 401:
            print("Correctly rejected unauthorized request")
        else:
            print(f"Unexpected response for unauthorized access: {response.status_code}")

    else:
        print(f"Login failed: {response.text}")
except Exception as e:
    print(f"Login or subsequent tests failed: {e}")

print("\nAPI testing completed!")