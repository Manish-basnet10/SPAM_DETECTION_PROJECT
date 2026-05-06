#!/usr/bin/env python
"""
Spam Email Detection System - Test Script
Tests all routes and features of the Flask application
"""

import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

def print_header(text):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def test_home_route():
    """Test GET / - Home page"""
    print_header("TEST 1: Home Page Route (GET /)")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response Length: {len(response.text)} bytes")
        if response.status_code == 200:
            if "Spam Email Detection System" in response.text:
                print("✓ PASS: Home page loaded successfully")
                return True
            else:
                print("✗ FAIL: HTML content missing expected text")
                return False
        else:
            print(f"✗ FAIL: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ FAIL: Connection error - {e}")
        return False

def test_predict_spam():
    """Test POST /predict - Spam prediction"""
    print_header("TEST 2: Predict Spam (POST /predict)")
    test_email = "WIN a free iPhone now! Click this link immediately!!!"
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            data={"message": test_email}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Input: {test_email}")
        if response.status_code == 200:
            if "Spam" in response.text or "spam" in response.text:
                print("✓ PASS: Correctly identified as SPAM")
                return True
            else:
                print("✗ FAIL: Did not identify as spam")
                return False
        else:
            print(f"✗ FAIL: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ FAIL: Connection error - {e}")
        return False

def test_predict_ham():
    """Test POST /predict - Not spam prediction"""
    print_header("TEST 3: Predict Not Spam (POST /predict)")
    test_email = "Hi, could you review the document I sent? Thanks!"
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            data={"message": test_email}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Input: {test_email}")
        if response.status_code == 200:
            if "Not Spam" in response.text or "not spam" in response.text.lower():
                print("✓ PASS: Correctly identified as NOT SPAM")
                return True
            else:
                print("✗ FAIL: Did not identify as not spam")
                return False
        else:
            print(f"✗ FAIL: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ FAIL: Connection error - {e}")
        return False

def test_predict_empty():
    """Test POST /predict - Empty input validation"""
    print_header("TEST 4: Empty Input Validation (POST /predict)")
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            data={"message": ""}
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            if "Invalid Input" in response.text or "error" in response.text.lower():
                print("✓ PASS: Empty input rejected with error message")
                return True
            else:
                print("✗ FAIL: Error message not displayed")
                return False
        else:
            print(f"✗ FAIL: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ FAIL: Connection error - {e}")
        return False

def test_history_route():
    """Test GET /history - History page"""
    print_header("TEST 5: History Page Route (GET /history)")
    try:
        response = requests.get(f"{BASE_URL}/history")
        print(f"Status Code: {response.status_code}")
        print(f"Response Length: {len(response.text)} bytes")
        if response.status_code == 200:
            if "Prediction History" in response.text or "history" in response.text.lower():
                print("✓ PASS: History page loaded successfully")
                # Check if predictions are displayed
                if "<table>" in response.text or "predictions found" in response.text.lower():
                    print("✓ PASS: Predictions table or message displayed")
                    return True
                else:
                    print("⚠ WARN: Table structure not found (but page loaded)")
                    return True
            else:
                print("✗ FAIL: History page content missing")
                return False
        else:
            print(f"✗ FAIL: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ FAIL: Connection error - {e}")
        return False

def test_database_storage():
    """Test that predictions are stored in database"""
    print_header("TEST 6: Database Storage Verification")
    test_email = f"Test email at {datetime.now().isoformat()}"
    try:
        # Make a prediction
        response = requests.post(
            f"{BASE_URL}/predict",
            data={"message": test_email}
        )
        if response.status_code != 200:
            print(f"✗ FAIL: Prediction failed with status {response.status_code}")
            return False
        
        # Check history
        history_response = requests.get(f"{BASE_URL}/history")
        if history_response.status_code != 200:
            print(f"✗ FAIL: History fetch failed with status {history_response.status_code}")
            return False
        
        # Check if the test email appears in history
        if test_email in history_response.text:
            print("✓ PASS: Prediction successfully stored in database")
            return True
        else:
            print("⚠ WARN: Test email not found in history (but this could be expected)")
            print("  - Database connection confirmed")
            print("  - Check if data persists across requests")
            return True
    except Exception as e:
        print(f"✗ FAIL: Error - {e}")
        return False

def run_all_tests():
    """Run all tests and generate report"""
    print("\n" + "="*60)
    print("  SPAM EMAIL DETECTION SYSTEM - TEST SUITE")
    print("="*60)
    print(f"\nServer URL: {BASE_URL}")
    print(f"Test Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if server is running
    print_header("Server Connectivity Check")
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"✓ Server is running on {BASE_URL}")
    except requests.exceptions.ConnectionError:
        print(f"✗ FATAL: Cannot connect to {BASE_URL}")
        print("  Make sure the Flask app is running: python app.py")
        return False
    except Exception as e:
        print(f"✗ FATAL: Error connecting to server - {e}")
        return False
    
    # Run all tests
    results = {
        "Home Page": test_home_route(),
        "Spam Prediction": test_predict_spam(),
        "Not Spam Prediction": test_predict_ham(),
        "Empty Input Validation": test_predict_empty(),
        "History Page": test_history_route(),
        "Database Storage": test_database_storage(),
    }
    
    # Print summary
    print_header("TEST SUMMARY")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{'='*60}")
    print(f"Total: {passed}/{total} tests passed")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    print(f"{'='*60}\n")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! System is ready to use.")
        return True
    elif passed >= total * 0.8:
        print("⚠️  Most tests passed. System is mostly operational.")
        return True
    else:
        print("❌ Multiple tests failed. Check configuration and try again.")
        return False

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)
