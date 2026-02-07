#!/usr/bin/env python3
"""
Test script to verify the Todo API security - ensuring users can't access other users' todos.
"""
import asyncio
import httpx
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

async def test_security():
    print("Testing Todo API security features...")

    # Create an async HTTP client
    async with httpx.AsyncClient(base_url=BASE_URL) as client:

        # Test 1: Create first user
        print("\n1. Creating first user...")
        user1_data = {
            "email": "user1@example.com",
            "password": "password123"
        }
        try:
            response = await client.post("/api/v1/auth/register", json=user1_data)
            print(f"User 1 registration: {response.status_code}")
            if response.status_code == 201:
                print("User 1 registered successfully")
            else:
                print(f"User 1 registration failed: {response.text}")
                return
        except Exception as e:
            print(f"User 1 registration failed: {e}")
            return

        # Test 2: Login as first user
        print("\n2. Logging in as first user...")
        login_data = {
            "username": "user1@example.com",
            "password": "password123"
        }
        try:
            response = await client.post("/api/v1/auth/login", data=login_data)
            print(f"User 1 login: {response.status_code}")
            if response.status_code == 200:
                user1_token = response.json()['access_token']
                user1_headers = {"Authorization": f"Bearer {user1_token}"}
                print("User 1 logged in successfully")
            else:
                print(f"User 1 login failed: {response.text}")
                return
        except Exception as e:
            print(f"User 1 login failed: {e}")
            return

        # Test 3: Create second user
        print("\n3. Creating second user...")
        user2_data = {
            "email": "user2@example.com",
            "password": "password123"
        }
        try:
            response = await client.post("/api/v1/auth/register", json=user2_data)
            print(f"User 2 registration: {response.status_code}")
            if response.status_code == 201:
                print("User 2 registered successfully")
            else:
                print(f"User 2 registration failed: {response.text}")
                return
        except Exception as e:
            print(f"User 2 registration failed: {e}")
            return

        # Test 4: Login as second user
        print("\n4. Logging in as second user...")
        login_data2 = {
            "username": "user2@example.com",
            "password": "password123"
        }
        try:
            response = await client.post("/api/v1/auth/login", data=login_data2)
            print(f"User 2 login: {response.status_code}")
            if response.status_code == 200:
                user2_token = response.json()['access_token']
                user2_headers = {"Authorization": f"Bearer {user2_token}"}
                print("User 2 logged in successfully")
            else:
                print(f"User 2 login failed: {response.text}")
                return
        except Exception as e:
            print(f"User 2 login failed: {e}")
            return

        # Test 5: User 1 creates a todo
        print("\n5. User 1 creating a todo...")
        todo_data = {
            "title": "User 1's Todo",
            "description": "This is user 1's personal todo"
        }
        try:
            response = await client.post("/api/v1/todos/", json=todo_data, headers=user1_headers)
            print(f"User 1 create todo: {response.status_code}")
            if response.status_code == 201:
                user1_todo = response.json()
                user1_todo_id = user1_todo['id']
                print(f"User 1's todo created: {user1_todo['title']} (ID: {user1_todo_id})")
            else:
                print(f"User 1 create todo failed: {response.text}")
                return
        except Exception as e:
            print(f"User 1 create todo failed: {e}")
            return

        # Test 6: User 2 creates a todo
        print("\n6. User 2 creating a todo...")
        todo_data2 = {
            "title": "User 2's Todo",
            "description": "This is user 2's personal todo"
        }
        try:
            response = await client.post("/api/v1/todos/", json=todo_data2, headers=user2_headers)
            print(f"User 2 create todo: {response.status_code}")
            if response.status_code == 201:
                user2_todo = response.json()
                user2_todo_id = user2_todo['id']
                print(f"User 2's todo created: {user2_todo['title']} (ID: {user2_todo_id})")
            else:
                print(f"User 2 create todo failed: {response.text}")
                return
        except Exception as e:
            print(f"User 2 create todo failed: {e}")
            return

        # Test 7: User 1 tries to access User 2's todo (should fail)
        print("\n7. Testing cross-user access - User 1 trying to access User 2's todo...")
        try:
            response = await client.get(f"/api/v1/todos/{user2_todo_id}", headers=user1_headers)
            print(f"User 1 accessing User 2's todo: {response.status_code}")
            if response.status_code in [403, 404]:
                print("✓ Security check passed - User 1 cannot access User 2's todo")
            else:
                print(f"✗ SECURITY VULNERABILITY - User 1 accessed User 2's todo: {response.text}")
        except Exception as e:
            print(f"Cross-user access test failed: {e}")

        # Test 8: User 2 tries to access User 1's todo (should fail)
        print("\n8. Testing cross-user access - User 2 trying to access User 1's todo...")
        try:
            response = await client.get(f"/api/v1/todos/{user1_todo_id}", headers=user2_headers)
            print(f"User 2 accessing User 1's todo: {response.status_code}")
            if response.status_code in [403, 404]:
                print("✓ Security check passed - User 2 cannot access User 1's todo")
            else:
                print(f"✗ SECURITY VULNERABILITY - User 2 accessed User 1's todo: {response.text}")
        except Exception as e:
            print(f"Cross-user access test failed: {e}")

        # Test 9: User 1 tries to update User 2's todo (should fail)
        print("\n9. Testing cross-user modification - User 1 trying to update User 2's todo...")
        update_data = {
            "title": "Hacked Todo",
            "description": "User 1 tried to modify User 2's todo"
        }
        try:
            response = await client.put(f"/api/v1/todos/{user2_todo_id}", json=update_data, headers=user1_headers)
            print(f"User 1 updating User 2's todo: {response.status_code}")
            if response.status_code in [403, 404]:
                print("✓ Security check passed - User 1 cannot update User 2's todo")
            else:
                print(f"✗ SECURITY VULNERABILITY - User 1 updated User 2's todo: {response.text}")
        except Exception as e:
            print(f"Cross-user update test failed: {e}")

        # Test 10: User 1 tries to delete User 2's todo (should fail)
        print("\n10. Testing cross-user deletion - User 1 trying to delete User 2's todo...")
        try:
            response = await client.delete(f"/api/v1/todos/{user2_todo_id}", headers=user1_headers)
            print(f"User 1 deleting User 2's todo: {response.status_code}")
            if response.status_code in [403, 404]:
                print("✓ Security check passed - User 1 cannot delete User 2's todo")
            else:
                print(f"✗ SECURITY VULNERABILITY - User 1 deleted User 2's todo: {response.text}")
        except Exception as e:
            print(f"Cross-user delete test failed: {e}")

        # Test 11: Verify each user can only see their own todos
        print("\n11. Testing todo isolation...")

        # Get User 1's todos
        try:
            response = await client.get("/api/v1/todos/", headers=user1_headers)
            print(f"User 1 getting own todos: {response.status_code}")
            if response.status_code == 200:
                user1_todos = response.json()
                print(f"User 1 has {len(user1_todos)} todos (should be 1)")
                if len(user1_todos) == 1 and user1_todos[0]['id'] == user1_todo_id:
                    print("✓ User 1 only sees their own todos")
                else:
                    print(f"✗ User 1 sees wrong todos: {user1_todos}")
            else:
                print(f"Failed to get User 1's todos: {response.text}")
        except Exception as e:
            print(f"Get User 1's todos failed: {e}")

        # Get User 2's todos
        try:
            response = await client.get("/api/v1/todos/", headers=user2_headers)
            print(f"User 2 getting own todos: {response.status_code}")
            if response.status_code == 200:
                user2_todos = response.json()
                print(f"User 2 has {len(user2_todos)} todos (should be 1)")
                if len(user2_todos) == 1 and user2_todos[0]['id'] == user2_todo_id:
                    print("✓ User 2 only sees their own todos")
                else:
                    print(f"✗ User 2 sees wrong todos: {user2_todos}")
            else:
                print(f"Failed to get User 2's todos: {response.text}")
        except Exception as e:
            print(f"Get User 2's todos failed: {e}")

        print("\nSecurity tests completed!")

if __name__ == "__main__":
    print("Starting security tests...")
    asyncio.run(test_security())
    print("\nSecurity tests finished!")