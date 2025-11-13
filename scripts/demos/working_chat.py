#!/usr/bin/env python3
"""
Working Chat Interface for HumAIne-chatbot
"""

import requests
import time

BASE_URL = "http://localhost:8000"

def working_chat():
    print("🚀 HumAIne-chatbot Working Chat")
    print("="*50)
    
    # Start conversation
    response = requests.post(f"{BASE_URL}/conversation/start", 
                           json={"user_id": "working_user"})
    data = response.json()
    session_id = data['session_id']
    
    print("✅ Conversation started!")
    print("💬 Type your questions below. Type 'quit' to exit.")
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
    working_chat() 