#!/usr/bin/env python3
"""
Demo Script for Expertise Elicitation and Prompt Comparison
"""

import requests
import time
import json

BASE_URL = "http://localhost:8000"

def demo_expertise_elicitation():
    print("🎯 DEMO: Expertise Elicitation & Prompt Comparison")
    print("="*70)
    
    # Start conversation
    response = requests.post(f"{BASE_URL}/conversation/start", 
                           json={"user_id": "demo_user"})
    data = response.json()
    session_id = data['session_id']
    
    print("✅ Conversation started!")
    print(f"Session ID: {session_id}")
    print("="*70)
    
    # Step 1: Ask main question
    main_question = "What are the best AI models for natural language processing?"
    print(f"\n👤 User asks: {main_question}")
    
    payload = {
        "session_id": session_id,
        "message": main_question,
        "typing_start_time": int(time.time() * 1000) - 5000,
        "typing_end_time": int(time.time() * 1000) - 1000
    }
    
    response = requests.post(f"{BASE_URL}/conversation/message", json=payload)
    data = response.json()
    
    print(f"\n🤖 Bot responds with expertise elicitation:")
    print(f"{data['response']}")
    
    # Step 2: Answer expertise questions
    expertise_answers = [
        "I'm an expert in this field",
        "I want comprehensive details",
        "I'm interested in practical applications"
    ]
    
    for i, answer in enumerate(expertise_answers, 1):
        print(f"\n👤 User answers expertise question {i}: {answer}")
        
        payload = {
            "session_id": session_id,
            "message": answer,
            "typing_start_time": int(time.time() * 1000) - 5000,
            "typing_end_time": int(time.time() * 1000) - 1000
        }
        
        response = requests.post(f"{BASE_URL}/conversation/message", json=payload)
        data = response.json()
        
        if 'metadata' in data and 'expertise_elicitation' in data['metadata']:
            print(f"\n🤖 Bot: {data['response']}")
        else:
            # Final response with prompt comparison
            print(f"\n🤖 Bot: {data['response']}")
            
            # Show prompt comparison
            if 'metadata' in data and 'raw_prompt' in data['metadata']:
                print(f"\n📊 PROMPT COMPARISON:")
                print(f"{'='*70}")
                print(f"🔍 RAW PROMPT:")
                print(f"{data['metadata']['raw_prompt']}")
                print(f"\n🎯 TAILORED PROMPT:")
                print(f"{data['metadata']['tailored_prompt']}")
                print(f"{'='*70}")
                
                # Show personalization info
                params = data['metadata']['personalization_params']
                print(f"\n📈 PERSONALIZATION PARAMETERS:")
                print(f"   Style: {params['response_style']}")
                print(f"   Detail: {params['detail_level']}")
                print(f"   Complexity: {params['language_complexity']}")
                print(f"   User Type: {params['user_type']}")
                print(f"   Engagement: {params['engagement_level']}")
    
    print(f"\n✅ Demo completed!")
    print("="*70)

if __name__ == "__main__":
    demo_expertise_elicitation() 