#!/usr/bin/env python3
"""
Enhanced System Test Script for HumAIne Chatbot

This script tests the enhanced user profile system, metrics collection,
and end-to-end scenarios to ensure everything is working properly.
"""

import requests
import json
import time
import uuid
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "test-api-key-123"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            print(f"   OpenAI: {data['openai']['status']}")
            print(f"   Active conversations: {data.get('active_conversations', 0)}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_user_profile_creation():
    """Test user profile creation and evolution"""
    print("\n👤 Testing User Profile Creation...")
    
    user_id = f"test-user-{int(time.time())}"
    session_id = f"test-session-{int(time.time())}"
    
    # Step 1: Send initial message to create profile
    print("   📤 Step 1: Sending initial message...")
    message_data = {
        "session_id": session_id,
        "user_id": user_id,
        "input_text": "Hello! I'm a new user testing the profile system.",
        "input_start_time": int(time.time() * 1000) - 5000,
        "input_end_time": int(time.time() * 1000) - 3000,
        "input_sent_time": int(time.time() * 1000) - 2000
    }
    
    try:
        response = requests.post(f"{BASE_URL}/interact", headers=HEADERS, json=message_data)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Message sent successfully: {data['message'][:100]}...")
        else:
            print(f"   ❌ Message failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Message error: {e}")
        return False
    
    # Step 2: Send feedback to update profile
    print("   📤 Step 2: Sending positive feedback...")
    feedback_data = {
        "session_id": session_id,
        "user_id": user_id,
        "response_text": "Hello! I'm a new user testing the profile system.",
        "response_start_time": int(time.time() * 1000) - 4000,
        "response_end_time": int(time.time() * 1000) - 2000,
        "response_duration": 2000,
        "feedback_type": "positive",
        "feedback_time": int(time.time() * 1000) - 1000,
        "feedback_delay_duration": 1000
    }
    
    try:
        response = requests.post(f"{BASE_URL}/feedback", headers=HEADERS, json=feedback_data)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Feedback sent successfully: {data['message']}")
        else:
            print(f"   ❌ Feedback failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Feedback error: {e}")
        return False
    
    # Step 3: End session to update profile
    print("   📤 Step 3: Ending session...")
    session_data = {
        "session_id": session_id,
        "user_id": user_id,
        "session_start": int(time.time() * 1000) - 10000,
        "session_end": int(time.time() * 1000),
        "session_end_type": "completed",
        "session_duration": 10000
    }
    
    try:
        response = requests.post(f"{BASE_URL}/session", headers=HEADERS, json=session_data)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Session ended successfully: {data['message']}")
        else:
            print(f"   ❌ Session failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Session error: {e}")
        return False
    
    # Step 4: Check user profile
    print("   📤 Step 4: Checking user profile...")
    try:
        response = requests.get(f"{BASE_URL}/profile/{user_id}", headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            profile = data['profile']
            print(f"   ✅ Profile retrieved successfully:")
            print(f"      - Sessions: {data['session_count']}")
            print(f"      - Feedback: {data['feedback_count']}")
            print(f"      - Preferred detail level: {profile['preferred_detail_level']}")
            print(f"      - Preferred response style: {profile['preferred_response_style']}")
        else:
            print(f"   ❌ Profile retrieval failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Profile retrieval error: {e}")
        return False
    
    return True

def test_enhanced_metrics():
    """Test the enhanced metrics collection system"""
    print("\n📊 Testing Enhanced Metrics Collection...")
    
    user_id = f"metrics-user-{int(time.time())}"
    session_id = f"metrics-session-{int(time.time())}"
    
    # Create some activity
    print("   📤 Creating test activity...")
    message_data = {
        "session_id": session_id,
        "user_id": user_id,
        "input_text": "Testing the metrics system with a longer message to analyze typing patterns and behavior.",
        "input_start_time": int(time.time() * 1000) - 8000,
        "input_end_time": int(time.time() * 1000) - 2000,
        "input_sent_time": int(time.time() * 1000) - 1000
    }
    
    try:
        response = requests.post(f"{BASE_URL}/interact", headers=HEADERS, json=message_data)
        if response.status_code == 200:
            print(f"   ✅ Test activity created")
        else:
            print(f"   ❌ Test activity failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Test activity error: {e}")
        return False
    
    # Test engagement metrics
    print("   📤 Testing engagement metrics...")
    try:
        response = requests.get(f"{BASE_URL}/metrics/engagement/{user_id}", headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            engagement = data['engagement_metrics']
            print(f"   ✅ Engagement metrics retrieved:")
            print(f"      - Active sessions: {engagement['active_sessions']}")
            print(f"      - Engagement score: {engagement['engagement_score']:.1f}")
            print(f"      - Total turns today: {engagement['total_turns_today']}")
        else:
            print(f"   ❌ Engagement metrics failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Engagement metrics error: {e}")
        return False
    
    # Test behavior metrics
    print("   📤 Testing behavior metrics...")
    try:
        response = requests.get(f"{BASE_URL}/metrics/behavior/{user_id}", headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            behavior = data['behavior_metrics']
            print(f"   ✅ Behavior metrics retrieved:")
            if 'typing_patterns' in behavior:
                typing = behavior['typing_patterns']
                print(f"      - Average typing duration: {typing.get('average_typing_duration', 0):.0f}ms")
                print(f"      - Message length variability: {typing.get('message_lengths', {}).get('length_variability', 0):.2f}")
        else:
            print(f"   ❌ Behavior metrics failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Behavior metrics error: {e}")
        return False
    
    # Test comprehensive metrics
    print("   📤 Testing comprehensive metrics...")
    try:
        response = requests.get(f"{BASE_URL}/metrics/comprehensive/{user_id}", headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            comprehensive = data['comprehensive_metrics']
            print(f"   ✅ Comprehensive metrics retrieved:")
            print(f"      - Total sessions: {comprehensive['summary']['total_sessions']}")
            print(f"      - Total interactions: {comprehensive['summary']['total_interactions']}")
            print(f"      - Feedback ratio: {comprehensive['summary']['feedback_ratio']:.2f}")
        else:
            print(f"   ❌ Comprehensive metrics failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Comprehensive metrics error: {e}")
        return False
    
    return True

def test_metrics_overview():
    """Test the metrics overview endpoint"""
    print("\n📈 Testing Metrics Overview...")
    
    try:
        response = requests.get(f"{BASE_URL}/metrics/overview", headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            overview = data['overview']
            print(f"   ✅ Metrics overview retrieved:")
            print(f"      - Active users: {overview['total_active_users']}")
            print(f"      - Active sessions: {overview['total_active_sessions']}")
            print(f"      - System health: {overview['system_health']}")
            return True
        else:
            print(f"   ❌ Metrics overview failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Metrics overview error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Enhanced System Test Suite")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("User Profile Creation", test_user_profile_creation),
        ("Enhanced Metrics Collection", test_enhanced_metrics),
        ("Metrics Overview", test_metrics_overview)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! The enhanced system is working perfectly!")
    else:
        print("⚠️  Some tests failed. Check the logs above for details.")
    
    return passed == len(results)

if __name__ == "__main__":
    main()
