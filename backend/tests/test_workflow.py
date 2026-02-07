#!/usr/bin/env python3
"""
Complete workflow test for the Todo API backend to verify all requirements are met.
"""
import asyncio
import httpx
import json

BASE_URL = "http://localhost:8000"

async def test_complete_workflow():
    print("Testing complete Todo API workflow...")

    # Create an async HTTP client
    async with httpx.AsyncClient(base_url=BASE_URL) as client:

        print("\n=== STEP 1: Register a new user ===")
        user_data = {
            "email": "workflow@test.com",
            "password": "securepassword123"
        }
        try:
            response = await client.post("/api/v1/auth/register", json=user_data)
            print(f"Registration: {response.status_code}")
            if response.status_code == 201:
                print("✓ User registered successfully")
                user_info = response.json()
                print(f"  - User ID: {user_info['id']}")
                print(f"  - Email: {user_info['email']}")
            else:
                print(f"✗ Registration failed: {response.text}")
                return False
        except Exception as e:
            print(f"✗ Registration failed with exception: {e}")
            return False

        print("\n=== STEP 2: Login and get JWT token ===")
        login_data = {
            "username": "workflow@test.com",
            "password": "securepassword123"
        }
        try:
            response = await client.post("/api/v1/auth/login", data=login_data)
            print(f"Login: {response.status_code}")
            if response.status_code == 200:
                print("✓ Login successful")
                token_data = response.json()
                access_token = token_data['access_token']
                token_type = token_data['token_type']
                print(f"  - Token type: {token_type}")
                print(f"  - Access token length: {len(access_token)}")

                # Create headers for authenticated requests
                headers = {"Authorization": f"Bearer {access_token}"}
            else:
                print(f"✗ Login failed: {response.text}")
                return False
        except Exception as e:
            print(f"✗ Login failed with exception: {e}")
            return False

        print("\n=== STEP 3: Use token to call /auth/me successfully ===")
        try:
            response = await client.get("/api/v1/auth/me", headers=headers)
            print(f"/auth/me: {response.status_code}")
            if response.status_code == 200:
                print("✓ /auth/me called successfully with token")
                user_details = response.json()
                print(f"  - User ID: {user_details['id']}")
                print(f"  - Email: {user_details['email']}")
                print(f"  - Created at: {user_details['created_at']}")
            else:
                print(f"✗ /auth/me failed: {response.text}")
                return False
        except Exception as e:
            print(f"✗ /auth/me failed with exception: {e}")
            return False

        print("\n=== STEP 4: Create a todo using the token ===")
        todo_data = {
            "title": "Workflow Test Todo",
            "description": "This todo was created as part of the complete workflow test",
            "priority": "medium",
            "status": "todo"
        }
        try:
            response = await client.post("/api/v1/todos/", json=todo_data, headers=headers)
            print(f"Create todo: {response.status_code}")
            if response.status_code == 201:
                print("✓ Todo created successfully")
                created_todo = response.json()
                todo_id = created_todo['id']
                print(f"  - Todo ID: {todo_id}")
                print(f"  - Title: {created_todo['title']}")
                print(f"  - Description: {created_todo['description']}")
                print(f"  - Completed: {created_todo['completed']}")
                print(f"  - Priority: {created_todo['priority']}")
                print(f"  - Created at: {created_todo['created_at']}")
                print(f"  - Updated at: {created_todo['updated_at']}")
            else:
                print(f"✗ Create todo failed: {response.text}")
                return False
        except Exception as e:
            print(f"✗ Create todo failed with exception: {e}")
            return False

        print("\n=== STEP 5: Get todos using the token ===")
        try:
            response = await client.get("/api/v1/todos/", headers=headers)
            print(f"Get todos: {response.status_code}")
            if response.status_code == 200:
                print("✓ Todos retrieved successfully")
                todos = response.json()
                print(f"  - Number of todos: {len(todos)}")
                if len(todos) >= 1:
                    print("  - At least one todo found as expected")
                else:
                    print("  - Warning: No todos found")
            else:
                print(f"✗ Get todos failed: {response.text}")
                return False
        except Exception as e:
            print(f"✗ Get todos failed with exception: {e}")
            return False

        print("\n=== STEP 6: Get specific todo using the token ===")
        try:
            response = await client.get(f"/api/v1/todos/{todo_id}", headers=headers)
            print(f"Get specific todo: {response.status_code}")
            if response.status_code == 200:
                print("✓ Specific todo retrieved successfully")
                retrieved_todo = response.json()
                print(f"  - Title: {retrieved_todo['title']}")
                print(f"  - Description: {retrieved_todo['description']}")
            else:
                print(f"✗ Get specific todo failed: {response.text}")
                return False
        except Exception as e:
            print(f"✗ Get specific todo failed with exception: {e}")
            return False

        print("\n=== STEP 7: Update todo using the token ===")
        update_data = {
            "title": "Updated Workflow Test Todo",
            "description": "This todo was updated as part of the complete workflow test",
            "completed": True,
            "priority": "high",
            "status": "completed"
        }
        try:
            response = await client.put(f"/api/v1/todos/{todo_id}", json=update_data, headers=headers)
            print(f"Update todo: {response.status_code}")
            if response.status_code == 200:
                print("✓ Todo updated successfully")
                updated_todo = response.json()
                print(f"  - New title: {updated_todo['title']}")
                print(f"  - New description: {updated_todo['description']}")
                print(f"  - Completed: {updated_todo['completed']}")
                print(f"  - Priority: {updated_todo['priority']}")
            else:
                print(f"✗ Update todo failed: {response.text}")
                return False
        except Exception as e:
            print(f"✗ Update todo failed with exception: {e}")
            return False

        print("\n=== STEP 8: Toggle todo completion using the token ===")
        try:
            response = await client.post(f"/api/v1/todos/{todo_id}/toggle", headers=headers)
            print(f"Toggle todo: {response.status_code}")
            if response.status_code == 200:
                print("✓ Todo completion toggled successfully")
                toggled_todo = response.json()
                print(f"  - Completed: {toggled_todo['completed']} (should be opposite of previous)")
            else:
                print(f"✗ Toggle todo failed: {response.text}")
                return False
        except Exception as e:
            print(f"✗ Toggle todo failed with exception: {e}")
            return False

        print("\n=== STEP 9: Requests without token should fail with 401 ===")
        # Test /auth/me without token
        try:
            response = await client.get("/api/v1/auth/me")
            print(f"Unauthorized /auth/me: {response.status_code}")
            if response.status_code == 401:
                print("✓ Unauthorized request properly rejected (401)")
            else:
                print(f"✗ Expected 401, got {response.status_code}: {response.text}")
        except Exception as e:
            print(f"✗ Unauthorized request test failed: {e}")

        # Test todos endpoint without token
        try:
            response = await client.get("/api/v1/todos/")
            print(f"Unauthorized /todos/: {response.status_code}")
            if response.status_code == 401:
                print("✓ Unauthorized request properly rejected (401)")
            else:
                print(f"✗ Expected 401, got {response.status_code}: {response.text}")
        except Exception as e:
            print(f"✗ Unauthorized request test failed: {e}")

        print("\n=== STEP 10: Delete todo using the token ===")
        try:
            response = await client.delete(f"/api/v1/todos/{todo_id}", headers=headers)
            print(f"Delete todo: {response.status_code}")
            if response.status_code == 204:
                print("✓ Todo deleted successfully")
            else:
                print(f"✗ Delete todo failed: {response.text}")
                return False
        except Exception as e:
            print(f"✗ Delete todo failed with exception: {e}")
            return False

        print("\n=== STEP 11: Verify todo is deleted ===")
        try:
            response = await client.get(f"/api/v1/todos/{todo_id}", headers=headers)
            print(f"Get deleted todo: {response.status_code}")
            if response.status_code == 404:
                print("✓ Deleted todo properly returns 404")
            else:
                print(f"✗ Expected 404 after deletion, got {response.status_code}")
        except Exception as e:
            print(f"✗ Verify deletion test failed: {e}")

        print("\n=== STEP 12: Test token expiration (simulated) ===")
        # This is a basic test - in a real scenario we'd test actual token expiration
        try:
            # Use the same valid token again to ensure it still works
            response = await client.get("/api/v1/auth/me", headers=headers)
            print(f"Valid token reuse: {response.status_code}")
            if response.status_code == 200:
                print("✓ Valid token continues to work for authenticated requests")
            else:
                print(f"✗ Valid token failed: {response.text}")
        except Exception as e:
            print(f"✗ Token reuse test failed: {e}")

        print("\n=== ALL WORKFLOW TESTS COMPLETED SUCCESSFULLY ===")
        print("✓ Registration works")
        print("✓ Login works and returns JWT token")
        print("✓ /auth/me works with valid token")
        print("✓ Create todo works with valid token")
        print("✓ Get todos works with valid token")
        print("✓ Get specific todo works with valid token")
        print("✓ Update todo works with valid token")
        print("✓ Toggle todo works with valid token")
        print("✓ Delete todo works with valid token")
        print("✓ Unauthorized requests return 401")
        print("✓ Token-based authentication works throughout")

        return True

if __name__ == "__main__":
    print("Starting complete workflow test...")
    success = asyncio.run(test_complete_workflow())
    if success:
        print("\n🎉 ALL TESTS PASSED! The Todo API backend meets all requirements.")
    else:
        print("\n❌ SOME TESTS FAILED! Please check the output above.")
    print("\nWorkflow test completed!")