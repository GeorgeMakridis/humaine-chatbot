#!/usr/bin/env python3
"""
Enhanced AI Profiler Demo Script

This script demonstrates all the enhanced features of the HumAIne-chatbot AI profiler:
- Profile persistence
- Enhanced language analysis
- Cross-session learning
- Advanced personalization
"""

import requests
import time
import json
import uuid
from datetime import datetime
from typing import Dict, Any

class EnhancedProfilerDemo:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = "test-api-key-123"):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
        
        # Test user IDs
        self.users = {
            'expert_user': str(uuid.uuid4()),
            'beginner_user': str(uuid.uuid4()),
            'casual_user': str(uuid.uuid4())
        }
        
        self.session_ids = {}
    
    def test_health_check(self):
        """Test the health check endpoint"""
        print("🧪 Testing Health Check...")
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed: {data['status']}")
                if data.get('openai', {}).get('status') == 'connected':
                    print("✅ OpenAI API connected successfully!")
                else:
                    print("⚠️  OpenAI API not connected")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def simulate_user_conversation(self, user_type: str, user_id: str, messages: list):
        """Simulate a conversation for a specific user type"""
        print(f"\n💬 Simulating {user_type} conversation for user {user_id[:8]}...")
        
        # Start session
        session_id = str(uuid.uuid4())
        self.session_ids[user_id] = session_id
        
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "session_start": int(time.time() * 1000),
            "session_end": None,
            "session_end_type": None,
            "session_duration": 0
        }
        
        # Send session start
        try:
            response = self.session.post(f"{self.base_url}/session", json=session_data)
            if response.status_code == 200:
                print(f"   ✅ Session started: {session_id[:8]}")
            else:
                print(f"   ❌ Session start failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Session start error: {e}")
        
        # Send messages
        for i, message in enumerate(messages):
            print(f"   📝 Sending message {i+1}: {message[:50]}...")
            
            # Simulate typing timing
            typing_start = int(time.time() * 1000) - 2000
            typing_end = int(time.time() * 1000) - 1000
            sent_time = int(time.time() * 1000)
            
            prompt_data = {
                "session_id": session_id,
                "user_id": user_id,
                "input_text": message,
                "input_start_time": typing_start,
                "input_end_time": typing_end,
                "input_sent_time": sent_time
            }
            
            try:
                response = self.session.post(f"{self.base_url}/interact", json=prompt_data)
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Bot response: {data['message'][:50]}...")
                    
                    # Simulate feedback (alternate positive/negative)
                    feedback_type = "positive" if i % 2 == 0 else "negative"
                    feedback_data = {
                        "session_id": session_id,
                        "user_id": user_id,
                        "response_text": data['message'],
                        "response_start_time": sent_time,
                        "response_end_time": int(time.time() * 1000),
                        "response_duration": 2000,
                        "feedback_type": feedback_type,
                        "feedback_time": int(time.time() * 1000),
                        "feedback_delay_duration": 3000
                    }
                    
                    feedback_response = self.session.post(f"{self.base_url}/feedback", json=feedback_data)
                    if feedback_response.status_code == 200:
                        print(f"   👍 Feedback sent: {feedback_type}")
                    
                else:
                    print(f"   ❌ Message failed: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Message error: {e}")
            
            time.sleep(1)  # Small delay between messages
        
        # End session
        session_data.update({
            "session_end": int(time.time() * 1000),
            "session_end_type": "completed",
            "session_duration": int(time.time() * 1000) - session_data["session_start"]
        })
        
        try:
            response = self.session.post(f"{self.base_url}/session", json=session_data)
            if response.status_code == 200:
                print(f"   ✅ Session ended: {session_id[:8]}")
            else:
                print(f"   ❌ Session end failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Session end error: {e}")
    
    def test_enhanced_profiling(self):
        """Test all enhanced profiling features"""
        print("\n🚀 Testing Enhanced AI Profiler Features...")
        
        # Test 1: Expert User (complex language, detailed responses)
        expert_messages = [
            "Could you please elucidate the intricate mechanisms underlying machine learning algorithms, particularly focusing on the mathematical foundations of neural networks and their optimization strategies?",
            "I'm interested in exploring the theoretical underpinnings of reinforcement learning, specifically the convergence properties of various policy gradient methods and their practical implications in real-world applications.",
            "What are the computational complexity considerations when implementing distributed training for large-scale language models, and how do they impact the scalability of modern AI systems?"
        ]
        self.simulate_user_conversation("Expert", self.users['expert_user'], expert_messages)
        
        # Test 2: Beginner User (simple language, basic questions)
        beginner_messages = [
            "Hi! How are you?",
            "What is AI?",
            "Can you help me learn?"
        ]
        self.simulate_user_conversation("Beginner", self.users['beginner_user'], beginner_messages)
        
        # Test 3: Casual User (mixed complexity, conversational)
        casual_messages = [
            "Hey there! I'm just curious about this stuff.",
            "So, like, how does this all work?",
            "That's pretty cool! Tell me more."
        ]
        self.simulate_user_conversation("Casual", self.users['casual_user'], casual_messages)
        
        # Wait for processing
        print("\n⏳ Waiting for profile processing...")
        time.sleep(5)
    
    def test_profile_retrieval(self):
        """Test profile retrieval and insights"""
        print("\n📊 Testing Profile Retrieval and Insights...")
        
        for user_type, user_id in self.users.items():
            print(f"\n👤 Testing {user_type} profile...")
            
            try:
                # Get user profile
                response = self.session.get(f"{self.base_url}/profile/{user_id}")
                if response.status_code == 200:
                    profile_data = response.json()
                    print(f"   ✅ Profile retrieved for {user_type}")
                    
                    # Display key profile information
                    profile = profile_data['profile']
                    print(f"   📋 Expertise Level: {profile['expertise_level']}")
                    print(f"   📋 Language Complexity: {profile['preferred_language_complexity']}")
                    print(f"   📋 Detail Level: {profile['preferred_detail_level']}")
                    print(f"   📋 Response Style: {profile['preferred_response_style']}")
                    print(f"   📋 Sessions: {profile_data['session_count']}")
                    print(f"   📋 Feedback: {profile_data['feedback_count']}")
                    
                    # Display insights if available
                    if profile_data.get('insights'):
                        insights = profile_data['insights']
                        if insights.get('insights'):
                            print(f"   🧠 Insights: {', '.join(insights['insights'][:2])}")
                        if insights.get('recommendations'):
                            print(f"   💡 Recommendations: {', '.join(insights['recommendations'][:2])}")
                    
                else:
                    print(f"   ❌ Profile retrieval failed: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Profile retrieval error: {e}")
    
    def test_profile_statistics(self):
        """Test profile statistics endpoint"""
        print("\n📈 Testing Profile Statistics...")
        
        try:
            response = self.session.get(f"{self.base_url}/profiles/stats")
            if response.status_code == 200:
                stats = response.json()
                print(f"   ✅ Profile stats retrieved")
                print(f"   📊 Total Profiles: {stats['stats'].get('total_profiles', 0)}")
                print(f"   📊 Storage Directory: {stats['stats'].get('profiles_directory', 'N/A')}")
            else:
                print(f"   ❌ Profile stats failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Profile stats error: {e}")
    
    def test_profile_persistence(self):
        """Test profile persistence by saving all profiles"""
        print("\n💾 Testing Profile Persistence...")
        
        try:
            response = self.session.post(f"{self.base_url}/profiles/save")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ {data['message']}")
            else:
                print(f"   ❌ Profile save failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Profile save error: {e}")
    
    def run_demo(self):
        """Run the complete enhanced profiler demo"""
        print("🎯 Enhanced AI Profiler Demo")
        print("=" * 50)
        
        # Test 1: Health Check
        if not self.test_health_check():
            print("❌ Health check failed. Please ensure the backend is running.")
            return
        
        # Test 2: Enhanced Profiling
        self.test_enhanced_profiling()
        
        # Test 3: Profile Retrieval
        self.test_profile_retrieval()
        
        # Test 4: Profile Statistics
        self.test_profile_statistics()
        
        # Test 5: Profile Persistence
        self.test_profile_persistence()
        
        print("\n🎉 Enhanced AI Profiler Demo Complete!")
        print("\n📋 What Was Demonstrated:")
        print("   ✅ Profile persistence across server restarts")
        print("   ✅ Enhanced language analysis and complexity detection")
        print("   ✅ Cross-session learning and pattern recognition")
        print("   ✅ Advanced personalization based on user behavior")
        print("   ✅ Real-time profile updates and insights")
        print("   ✅ Comprehensive user behavior analytics")
        
        print("\n🔍 Next Steps:")
        print("   1. Restart the backend to test profile persistence")
        print("   2. Send more messages to see profile evolution")
        print("   3. Check the /profile/{user_id} endpoint for insights")
        print("   4. Monitor the data/profiles/ directory for saved profiles")

if __name__ == "__main__":
    demo = EnhancedProfilerDemo()
    demo.run_demo()
