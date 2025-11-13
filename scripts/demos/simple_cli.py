#!/usr/bin/env python3
"""
Simple CLI for HumAIne-chatbot Testing

This script provides a simple interactive interface to test the chatbot.
"""

import requests
import json
import time
import sys

# Base URL for the API
BASE_URL = "http://localhost:8000"

def check_health():
    """Check if the chatbot is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ HumAIne-chatbot is running!")
            print(f"   Status: {health_data['status']}")
            print(f"   Active conversations: {health_data['active_conversations']}")
            return True
        else:
            print("❌ HumAIne-chatbot is not responding")
            return False
    except Exception as e:
        print(f"❌ Error connecting to HumAIne-chatbot: {e}")
        return False

def start_conversation(user_id=None):
    """Start a new conversation"""
    if not user_id:
        user_id = f"cli_user_{int(time.time())}"
    
    try:
        response = requests.post(f"{BASE_URL}/conversation/start", 
                              json={"user_id": user_id})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Conversation started!")
            print(f"   Session ID: {data['session_id']}")
            print(f"   User ID: {user_id}")
            return data['session_id'], user_id
        else:
            print(f"❌ Failed to start conversation: {response.text}")
            return None, None
    except Exception as e:
        print(f"❌ Error starting conversation: {e}")
        return None, None

def send_message(session_id, message):
    """Send a message to the chatbot"""
    try:
        payload = {
            "session_id": session_id,
            "message": message,
            "typing_start_time": int(time.time() * 1000) - 5000,
            "typing_end_time": int(time.time() * 1000) - 1000
        }
        
        response = requests.post(f"{BASE_URL}/conversation/message", json=payload)
        if response.status_code == 200:
            data = response.json()
            
            # Print the response
            print(f"\n🤖 Bot Response:")
            print(f"{'='*60}")
            print(data['response'])
            print(f"{'='*60}")
            
            # Print personalization info
            params = data['metadata']['personalization_params']
            print(f"\n📊 Personalization:")
            print(f"   Style: {params['response_style']}")
            print(f"   Detail: {params['detail_level']}")
            print(f"   Complexity: {params['language_complexity']}")
            print(f"   User Type: {params['user_type']}")
            print(f"   Engagement: {params['engagement_level']}")
            
            return True
        else:
            print(f"❌ Failed to send message: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False

def main():
    """Main function"""
    print("🚀 HumAIne-chatbot Simple CLI")
    print("="*60)
    
    # Check if chatbot is running
    if not check_health():
        print("❌ Cannot connect to HumAIne-chatbot. Make sure it's running!")
        sys.exit(1)
    
    # Start conversation
    session_id, user_id = start_conversation()
    if not session_id:
        print("❌ Failed to start conversation")
        sys.exit(1)
    
    print(f"\n💬 You can now chat with the HumAIne-chatbot!")
    print(f"Type your messages below. Type 'quit' to exit.")
    print(f"="*60)
    
    # Chat loop
    while True:
        try:
            message = input("\n👤 You: ").strip()
            
            if not message:
                continue
            
            if message.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            # Send message
            send_message(session_id, message)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 