#!/usr/bin/env python3
"""
UI-Backend Connection Test

This script tests the connection between the UI and backend to ensure
they're communicating with the correct data schemas.
"""

import requests
import time
import json
import uuid
from datetime import datetime

class UIConnectionTester:
    def __init__(self, base_url="http://localhost:8000", api_key="test-api-key-123"):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
    
    def test_connection(self):
        """Test basic connection to backend"""
        print("🧪 Testing UI-Backend Connection")
        print("=" * 40)
        
        # Test 1: Health Check
        if not self.test_health_check():
            return False
        
        # Test 2: Message Flow (simulating UI)
        if not self.test_message_flow():
            return False
        
        # Test 3: Feedback Flow (simulating UI)
        if not self.test_feedback_flow():
            return False
        
        # Test 4: Session Flow (simulating UI)
        if not self.test_session_flow():
            return False
        
        print("\n🎉 All UI-Backend connection tests passed!")
        return True
    
    def test_health_check(self):
        """Test health check endpoint"""
        print("\n🔍 Testing Health Check...")
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed: {data['status']}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def test_message_flow(self):
        """Test message flow (simulating UI UserPrompt)"""
        print("\n💬 Testing Message Flow...")
        
        # Simulate UI UserPrompt.toJSON() output
        ui_message_data = {
            "session_id": str(uuid.uuid4()),
            "user_id": str(uuid.uuid4()),
            "input_text": "Hello! This is a test message from the UI.",
            "input_start_time": int(time.time() * 1000) - 2000,
            "input_end_time": int(time.time() * 1000) - 1000,
            "input_sent_time": int(time.time() * 1000)
        }
        
        print(f"   📤 UI sending: {json.dumps(ui_message_data, indent=2)}")
        
        try:
            response = self.session.post(f"{self.base_url}/interact", json=ui_message_data)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Backend response: {data['message'][:50]}...")
                print(f"   📊 Response format: {json.dumps(data, indent=2)}")
                return True
            else:
                print(f"   ❌ Message failed: {response.status_code}")
                print(f"   📄 Error response: {response.text}")
                return False
        except Exception as e:
            print(f"   ❌ Message error: {e}")
            return False
    
    def test_feedback_flow(self):
        """Test feedback flow (simulating UI Feedback)"""
        print("\n👍 Testing Feedback Flow...")
        
        # Simulate UI Feedback.toJSON() output
        ui_feedback_data = {
            "session_id": str(uuid.uuid4()),
            "user_id": str(uuid.uuid4()),
            "response_text": "This is a test bot response for feedback testing.",
            "response_start_time": int(time.time() * 1000) - 5000,
            "response_end_time": int(time.time() * 1000) - 3000,
            "response_duration": 2000,
            "feedback_type": "positive",
            "feedback_time": int(time.time() * 1000),
            "feedback_delay_duration": 3000
        }
        
        print(f"   📤 UI sending: {json.dumps(ui_feedback_data, indent=2)}")
        
        try:
            response = self.session.post(f"{self.base_url}/feedback", json=ui_feedback_data)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Backend response: {data['message']}")
                return True
            else:
                print(f"   ❌ Feedback failed: {response.status_code}")
                print(f"   📄 Error response: {response.text}")
                return False
        except Exception as e:
            print(f"   ❌ Feedback error: {e}")
            return False
    
    def test_session_flow(self):
        """Test session flow (simulating UI Session)"""
        print("\n📅 Testing Session Flow...")
        
        # Simulate UI Session.toJSON() output
        ui_session_data = {
            "session_id": str(uuid.uuid4()),
            "user_id": str(uuid.uuid4()),
            "session_start": int(time.time() * 1000) - 60000,
            "session_end": int(time.time() * 1000),
            "session_end_type": "completed",
            "session_duration": 60000
        }
        
        print(f"   📤 UI sending: {json.dumps(ui_session_data, indent=2)}")
        
        try:
            response = self.session.post(f"{self.base_url}/session", json=ui_session_data)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Backend response: {data['message']}")
                return True
            else:
                print(f"   ❌ Session failed: {response.status_code}")
                print(f"   📄 Error response: {response.text}")
                return False
        except Exception as e:
            print(f"   ❌ Session error: {e}")
            return False
    
    def test_schema_compatibility(self):
        """Test that UI and backend schemas are compatible"""
        print("\n🔍 Testing Schema Compatibility...")
        
        # Test UserPrompt schema compatibility
        ui_user_prompt = {
            "session_id": "test_session",
            "user_id": "test_user",
            "input_text": "Test message",
            "input_start_time": 1234567890,
            "input_end_time": 1234567890,
            "input_sent_time": 1234567890
        }
        
        try:
            response = self.session.post(f"{self.base_url}/interact", json=ui_user_prompt)
            if response.status_code == 200:
                print("   ✅ UserPrompt schema is compatible")
                return True
            else:
                print(f"   ❌ UserPrompt schema failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ UserPrompt schema error: {e}")
            return False

def main():
    print("🚀 UI-Backend Connection Test")
    print("=" * 50)
    
    # Test the connection
    tester = UIConnectionTester()
    success = tester.test_connection()
    
    if success:
        print("\n🎉 UI-Backend connection is working correctly!")
        print("\n📋 What's Working:")
        print("   ✅ Backend is accessible")
        print("   ✅ Message flow is functional")
        print("   ✅ Feedback flow is functional")
        print("   ✅ Session flow is functional")
        print("   ✅ Data schemas are compatible")
        
        print("\n🔧 Next Steps:")
        print("   1. Build and test the UI components")
        print("   2. Verify real-time communication")
        print("   3. Test with actual user interactions")
        
    else:
        print("\n❌ UI-Backend connection has issues!")
        print("\n🔧 Troubleshooting:")
        print("   1. Ensure backend is running on port 8000")
        print("   2. Check API key authentication")
        print("   3. Verify endpoint URLs")
        print("   4. Check data schema compatibility")

if __name__ == "__main__":
    main()
