#!/usr/bin/env python3
"""
Simple Chat Interface for HumAIne-chatbot - Command Line Version
"""

import requests
import time
import sys

BASE_URL = "http://localhost:8000"

def simple_chat():
    print("🚀 HumAIne-chatbot Simple Chat")
    print("="*50)
    
    # Check if chatbot is running
    try:
        health_response = requests.get(f"{BASE_URL}/health")
        if health_response.status_code == 200:
            print("✅ HumAIne-chatbot is running!")
        else:
            print("❌ HumAIne-chatbot is not responding")
            return
    except Exception as e:
        print(f"❌ Cannot connect to HumAIne-chatbot: {e}")
        return
    
    # Start conversation
    try:
        response = requests.post(f"{BASE_URL}/conversation/start", 
                               json={"user_id": "simple_chat_user"})
        data = response.json()
        session_id = data['session_id']
        print(f"✅ Conversation started! Session: {session_id}")
    except Exception as e:
        print(f"❌ Failed to start conversation: {e}")
        return
    
    print("\n💬 Type your messages below. Type 'quit' to exit.")
    print("="*50)
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ")
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            # Send message
            payload = {
                "session_id": session_id,
                "message": user_input,
                "typing_start_time": int(time.time() * 1000) - 5000,
                "typing_end_time": int(time.time() * 1000) - 1000
            }
            
            response = requests.post(f"{BASE_URL}/conversation/message", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n🤖 Bot: {data['response']}")
                
                # Show prompt comparison if available
                if 'metadata' in data and 'raw_prompt' in data['metadata']:
                    print(f"\n📊 PROMPT COMPARISON:")
                    print(f"🔍 RAW: {data['metadata']['raw_prompt']}")
                    print(f"🎯 TAILORED: {data['metadata']['tailored_prompt']}")
                    
                    params = data['metadata']['personalization_params']
                    print(f"📈 Style: {params['response_style']}, Detail: {params['detail_level']}, Complexity: {params['language_complexity']}")
            else:
                print(f"❌ Error: {response.text}")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    simple_chat() 