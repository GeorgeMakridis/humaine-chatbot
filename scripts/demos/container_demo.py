"""
Container Demo for HumAIne-chatbot

This script demonstrates the working functionality of the containerized
HumAIne-chatbot system.
"""

import requests
import json
import time


def demo_container_functionality():
    """Demonstrate the working container functionality"""
    print("🚀 HumAIne-Chatbot Container Demo")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed!")
            print(f"   Status: {data['status']}")
            print(f"   Active conversations: {data['active_conversations']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Root Endpoint
    print("\n2️⃣ Testing Root Endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint working!")
            print(f"   Message: {data['message']}")
            print(f"   Version: {data['version']}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False
    
    # Test 3: Start Conversation
    print("\n3️⃣ Testing Conversation Start...")
    try:
        start_data = {
            "user_id": "demo_user_001",
            "initial_context": {"domain": "technology", "topic": "AI"}
        }
        response = requests.post(f"{base_url}/conversation/start", json=start_data)
        if response.status_code == 200:
            data = response.json()
            session_id = data["session_id"]
            print(f"✅ Conversation started!")
            print(f"   Session ID: {session_id}")
            print(f"   Status: {data['status']}")
        else:
            print(f"❌ Conversation start failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Conversation start error: {e}")
        return False
    
    # Test 4: Get User Profile
    print("\n4️⃣ Testing User Profile...")
    try:
        response = requests.get(f"{base_url}/user/demo_user_001/profile")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ User profile retrieved!")
            print(f"   User ID: {data['user_id']}")
            profile = data['profile']
            if 'personalization_params' in profile:
                params = profile['personalization_params']
                print(f"   Language complexity: {params.get('language_complexity', 'N/A')}")
                print(f"   Response style: {params.get('response_style', 'N/A')}")
        else:
            print(f"⚠️  User profile not found (expected for new user): {response.status_code}")
    except Exception as e:
        print(f"⚠️  User profile error: {e}")
    
    # Test 5: API Documentation
    print("\n5️⃣ Testing API Documentation...")
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print(f"✅ API documentation available!")
            print(f"   📚 Swagger UI: http://localhost:8000/docs")
            print(f"   📖 ReDoc: http://localhost:8000/redoc")
        else:
            print(f"⚠️  API docs not available: {response.status_code}")
    except Exception as e:
        print(f"⚠️  API docs error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Container Demo Completed Successfully!")
    print("\n💡 The HumAIne-chatbot container is working correctly!")
    print("\n📋 Available Endpoints:")
    print("   • GET  /health - Health check")
    print("   • GET  / - Root endpoint")
    print("   • POST /conversation/start - Start conversation")
    print("   • POST /conversation/message - Send message")
    print("   • POST /conversation/feedback - Record feedback")
    print("   • POST /conversation/end - End conversation")
    print("   • GET  /user/{user_id}/profile - Get user profile")
    print("   • GET  /docs - API documentation")
    
    print("\n🔧 Container Management:")
    print("   • View logs: docker logs humaine-chatbot-backend")
    print("   • Stop container: docker stop humaine-chatbot-backend")
    print("   • Restart container: docker restart humaine-chatbot-backend")
    print("   • Remove container: docker rm humaine-chatbot-backend")
    
    print("\n🌐 Access Points:")
    print("   • API: http://localhost:8000")
    print("   • Documentation: http://localhost:8000/docs")
    print("   • Health Check: http://localhost:8000/health")
    
    return True


if __name__ == "__main__":
    demo_container_functionality() 