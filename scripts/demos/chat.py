#!/usr/bin/env python3
"""
Enhanced Chat Interface for HumAIne-chatbot with Expertise Elicitation
"""

import requests
import time

BASE_URL = "http://localhost:8000"

def chat():
    print("🚀 HumAIne-chatbot Enhanced Chat Interface")
    print("="*60)
    print("💡 The bot will ask 2-3 questions to understand your expertise level")
    print("💡 Then it will show you the raw vs tailored prompts")
    print("="*60)
    
    # Start conversation
    response = requests.post(f"{BASE_URL}/conversation/start", 
                           json={"user_id": "expertise_test_user"})
    data = response.json()
    session_id = data['session_id']
    
    print("✅ Conversation started!")
    print("💬 Type your main question below. Type 'quit' to exit.")
    print("="*60)
    
    while True:
        try:
            # Get user input
            message = input("\n👤 You: ").strip()
            
            if message.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            if not message:
                continue
            
            # Send message
            payload = {
                "session_id": session_id,
                "message": message,
                "typing_start_time": int(time.time() * 1000) - 5000,
                "typing_end_time": int(time.time() * 1000) - 1000
            }
            
            response = requests.post(f"{BASE_URL}/conversation/message", json=payload)
            data = response.json()
            
            # Show bot response
            print(f"\n🤖 Bot: {data['response']}")
            
            # Show prompt comparison if available
            if 'metadata' in data and 'raw_prompt' in data['metadata']:
                print(f"\n📊 PROMPT COMPARISON:")
                print(f"{'='*60}")
                print(f"🔍 RAW PROMPT:")
                print(f"{data['metadata']['raw_prompt']}")
                print(f"\n🎯 TAILORED PROMPT:")
                print(f"{data['metadata']['tailored_prompt']}")
                print(f"{'='*60}")
                
                # Show personalization info
                params = data['metadata']['personalization_params']
                print(f"\n📈 PERSONALIZATION PARAMETERS:")
                print(f"   Style: {params['response_style']}")
                print(f"   Detail: {params['detail_level']}")
                print(f"   Complexity: {params['language_complexity']}")
                print(f"   User Type: {params['user_type']}")
                print(f"   Engagement: {params['engagement_level']}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    chat() 