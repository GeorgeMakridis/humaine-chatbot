"""
Container Test Script for HumAIne-chatbot

This script tests the containerized HumAIne-chatbot system
by making API calls to the running container.
"""

import requests
import time
import json
from datetime import datetime


class ContainerTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_health_check(self):
        """Test the health check endpoint"""
        print("🧪 Testing Health Check...")
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed: {data}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def test_root_endpoint(self):
        """Test the root endpoint"""
        print("\n🧪 Testing Root Endpoint...")
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Root endpoint: {data}")
                return True
            else:
                print(f"❌ Root endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Root endpoint error: {e}")
            return False
    
    def test_conversation_flow(self):
        """Test complete conversation flow"""
        print("\n🧪 Testing Conversation Flow...")
        
        # Start conversation
        print("   Starting conversation...")
        start_data = {
            "user_id": "container_test_user",
            "initial_context": {"domain": "technology", "topic": "AI"}
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/conversation/start",
                json=start_data
            )
            
            if response.status_code == 200:
                session_data = response.json()
                session_id = session_data["session_id"]
                print(f"   ✅ Conversation started: {session_id}")
            else:
                print(f"   ❌ Failed to start conversation: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Start conversation error: {e}")
            return False
        
        # Send messages
        test_messages = [
            "Hello! I'm interested in learning about AI.",
            "Can you explain what machine learning is?",
            "What are some practical applications?",
            "How can I get started with AI?"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"   Sending message {i}: {message[:30]}...")
            
            message_data = {
                "session_id": session_id,
                "message": message,
                "typing_start_time": int(time.time() * 1000) - 2000,
                "typing_end_time": int(time.time() * 1000) - 1000,
                "bot_message_time": int(time.time() * 1000)
            }
            
            try:
                response = self.session.post(
                    f"{self.base_url}/conversation/message",
                    json=message_data
                )
                
                if response.status_code == 200:
                    response_data = response.json()
                    bot_response = response_data["response"]
                    metadata = response_data["metadata"]
                    
                    print(f"   ✅ Bot response: {bot_response[:50]}...")
                    print(f"      Style: {metadata.get('personalization_params', {}).get('response_style', 'unknown')}")
                    
                    # Record feedback
                    feedback_data = {
                        "session_id": session_id,
                        "response_text": bot_response,
                        "feedback_type": "positive" if i % 2 == 0 else "negative",
                        "response_start_time": int(time.time() * 1000) - 1000,
                        "response_end_time": int(time.time() * 1000)
                    }
                    
                    feedback_response = self.session.post(
                        f"{self.base_url}/conversation/feedback",
                        json=feedback_data
                    )
                    
                    if feedback_response.status_code == 200:
                        print(f"      ✅ Feedback recorded: {feedback_data['feedback_type']}")
                    else:
                        print(f"      ⚠️  Feedback failed: {feedback_response.status_code}")
                    
                else:
                    print(f"   ❌ Message failed: {response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"   ❌ Message error: {e}")
                return False
            
            time.sleep(1)  # Small delay between messages
        
        # End conversation
        print("   Ending conversation...")
        end_data = {
            "session_id": session_id,
            "end_type": "userAction"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/conversation/end",
                json=end_data
            )
            
            if response.status_code == 200:
                end_data = response.json()
                print(f"   ✅ Conversation ended: {end_data}")
                return True
            else:
                print(f"   ❌ Failed to end conversation: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ End conversation error: {e}")
            return False
    
    def test_user_profile(self):
        """Test user profile functionality"""
        print("\n🧪 Testing User Profile...")
        
        user_id = "container_test_user"
        
        try:
            response = self.session.get(f"{self.base_url}/user/{user_id}/profile")
            
            if response.status_code == 200:
                profile_data = response.json()
                profile = profile_data["profile"]
                print(f"✅ User profile retrieved:")
                print(f"   - User ID: {profile_data['user_id']}")
                print(f"   - Profile data: {len(profile)} fields")
                return True
            else:
                print(f"❌ Failed to get user profile: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ User profile error: {e}")
            return False
    
    def test_conversation_analytics(self):
        """Test conversation analytics"""
        print("\n🧪 Testing Conversation Analytics...")
        
        # First start a conversation to have data
        start_data = {"user_id": "analytics_test_user"}
        response = self.session.post(f"{self.base_url}/conversation/start", json=start_data)
        
        if response.status_code == 200:
            session_id = response.json()["session_id"]
            
            # Send a message
            message_data = {
                "session_id": session_id,
                "message": "Test message for analytics"
            }
            self.session.post(f"{self.base_url}/conversation/message", json=message_data)
            
            # Get analytics
            try:
                response = self.session.get(f"{self.base_url}/conversation/{session_id}/analytics")
                
                if response.status_code == 200:
                    analytics = response.json()
                    print(f"✅ Analytics retrieved: {len(analytics)} metrics")
                    return True
                else:
                    print(f"❌ Failed to get analytics: {response.status_code}")
                    return False
            except Exception as e:
                print(f"❌ Analytics error: {e}")
                return False
        else:
            print("❌ Could not start conversation for analytics test")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 HumAIne-Chatbot Container Test")
        print("=" * 50)
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Root Endpoint", self.test_root_endpoint),
            ("Conversation Flow", self.test_conversation_flow),
            ("User Profile", self.test_user_profile),
            ("Conversation Analytics", self.test_conversation_analytics)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                print(f"\n{'='*20} {test_name} {'='*20}")
                if test_func():
                    passed += 1
                    print(f"✅ {test_name} PASSED")
                else:
                    print(f"❌ {test_name} FAILED")
            except Exception as e:
                print(f"❌ {test_name} ERROR: {e}")
        
        print(f"\n{'='*50}")
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! The container is working correctly.")
        else:
            print("⚠️  Some tests failed. Please check the container logs.")
        
        return passed == total


def main():
    """Main function"""
    print("🔧 Starting container test...")
    
    # Wait for container to be ready
    print("⏳ Waiting for container to be ready...")
    time.sleep(10)
    
    tester = ContainerTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n💡 Container test completed successfully!")
        print("   The HumAIne-chatbot backend is running properly in the container.")
    else:
        print("\n⚠️  Container test had issues.")
        print("   Check the container logs: docker logs humaine-chatbot-backend")


if __name__ == "__main__":
    main() 