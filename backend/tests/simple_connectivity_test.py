import requests
import time

# Give the server some time to start
time.sleep(3)

try:
    # Test health endpoint
    response = requests.get("http://127.0.0.1:8001/health")
    print(f"Health check: {response.status_code} - {response.json()}")

    # Test root endpoint
    response = requests.get("http://127.0.0.1:8001/")
    print(f"Root endpoint: {response.status_code} - {response.json()}")

    print("Basic connectivity test passed!")

except Exception as e:
    print(f"Test failed with error: {e}")