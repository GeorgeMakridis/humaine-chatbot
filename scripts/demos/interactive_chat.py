#!/usr/bin/env python3
"""
Interactive Chat for HumAIne-chatbot - Command Line Testing
"""

import requests
import time

BASE_URL = "http://localhost:8000"

def interactive_chat():
    print("🚀 HumAIne-chatbot Interactive Chat")
    print("="*60)
    print("💡 This will demonstrate expertise elicitation and prompt comparison")
    print("💡 Type your questions and see how the system adapts!")
    print("="*60)
    
    # Start conversation
    response = requests.post(f"{BASE_URL}/conversation/start", 
                           json={"user_id": "interactive_user"})
    data = response.json()
    session_id = data['session_id']
    
    print("✅ Conversation started!")
    print("💬 Type your questions below. Type 'quit' to exit.")
    print("="*60)
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
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
                    print(f"{'='*50}")
                    print(f"🔍 RAW PROMPT:")
                    print(f"{data['metadata']['raw_prompt']}")
                    print(f"\n🎯 TAILORED PROMPT:")
                    print(f"{data['metadata']['tailored_prompt']}")
                    print(f"{'='*50}")
                    
                    # Show personalization
                    params = data['metadata']['personalization_params']
                    print(f"\n📈 PERSONALIZATION:")
                    print(f"   Style: {params['response_style']}")
                    print(f"   Detail: {params['detail_level']}")
                    print(f"   Complexity: {params['language_complexity']}")
                    print(f"   User Type: {params['user_type']}")
                    print(f"   Engagement: {params['engagement_level']}")
            else:
                print(f"❌ Error: {response.text}")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    interactive_chat() 