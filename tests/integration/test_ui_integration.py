#!/usr/bin/env python3
"""
Test script to verify the backend works with the exact UI data structures
"""

import asyncio
import json
import requests
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:8000"
API_KEY = "test-api-key-123"

def test_backend_endpoints():
    """Test all backend endpoints with exact UI data structures"""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    print("🧪 Testing HumAIne Backend Integration")
    print("=" * 50)
    
    # Test 1: Root endpoint
    print("\n1️⃣ Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test 2: UserPrompt endpoint (matches UserPrompt.toJSON() exactly)
    print("\n2️⃣ Testing UserPrompt endpoint...")
    user_prompt_data = {
        "session_id": "test_session_123",
        "user_id": "test_user_456",
        "input_text": "Hello, how are you today?",
        "input_start_time": int(datetime.now().timestamp() * 1000) - 5000,  # 5 seconds ago
        "input_end_time": int(datetime.now().timestamp() * 1000) - 3000,   # 3 seconds ago
        "input_sent_time": int(datetime.now().timestamp() * 1000)
        # Note: This matches exactly what UserPrompt.toJSON() sends
        # Additional metrics from userMessage.metrics are not included in this test
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/interact",
            headers=headers,
            json=user_prompt_data
        )
        if response.status_code == 200:
            print("✅ UserPrompt endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ UserPrompt endpoint failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ UserPrompt endpoint error: {e}")
    
    # Test 3: Feedback endpoint (matches Feedback.toJSON())
    print("\n3️⃣ Testing Feedback endpoint...")
    feedback_data = {
        "session_id": "test_session_123",
        "user_id": "test_user_456",
        "response_text": "I'm doing well, thank you for asking!",
        "response_start_time": int(datetime.now().timestamp() * 1000) - 2000,
        "response_end_time": int(datetime.now().timestamp() * 1000) - 1000,
        "response_duration": 1000,
        "feedback_type": "positive",
        "feedback_time": int(datetime.now().timestamp() * 1000),
        "feedback_delay_duration": 500
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/feedback",
            headers=headers,
            json=feedback_data
        )
        if response.status_code == 200:
            print("✅ Feedback endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Feedback endpoint failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Feedback endpoint error: {e}")
    
    # Test 4: Session endpoint (matches Session.toJSON())
    print("\n4️⃣ Testing Session endpoint...")
    session_data = {
        "session_id": "test_session_123",
        "user_id": "test_user_456",
        "session_start": int(datetime.now().timestamp() * 1000) - 10000,
        "session_end": int(datetime.now().timestamp() * 1000),
        "session_end_type": "userAction",
        "session_duration": 10000
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/session",
            headers=headers,
            json=session_data
        )
        if response.status_code == 200:
            print("✅ Session endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Session endpoint failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Session endpoint error: {e}")
    
    # Test 5: Invalid API key
    print("\n5️⃣ Testing invalid API key...")
    invalid_headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer invalid-key"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/interact",
            headers=invalid_headers,
            json=user_prompt_data
        )
        if response.status_code == 401:
            print("✅ Invalid API key properly rejected")
        else:
            print(f"❌ Invalid API key not properly rejected: {response.status_code}")
    except Exception as e:
        print(f"❌ Invalid API key test error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Testing completed!")

if __name__ == "__main__":
    test_backend_endpoints()
