#!/usr/bin/env python
"""Test the Flask API endpoints"""

import json
import requests

BASE_URL = "http://127.0.0.1:5000"

print("Testing Flask API...")
print("=" * 60)

# Test 1: Home endpoint
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"GET /")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
except Exception as e:
    print(f"Error testing home endpoint: {e}")
    print()

# Test 2: Health endpoint
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"GET /health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
except Exception as e:
    print(f"Error testing health endpoint: {e}")
    print()

# Test 3: Spam prediction
try:
    payload = {"message": "Win free money now! Call 1234567"}
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"POST /predict")
    print(f"Request: {json.dumps(payload, indent=2)}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
except Exception as e:
    print(f"Error testing predict endpoint: {e}")
    print()

# Test 4: Non-spam prediction
try:
    payload = {"message": "Hey, how are you doing today?"}
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"POST /predict")
    print(f"Request: {json.dumps(payload, indent=2)}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
except Exception as e:
    print(f"Error testing predict endpoint: {e}")
    print()

print("=" * 60)
print("Testing completed!")
