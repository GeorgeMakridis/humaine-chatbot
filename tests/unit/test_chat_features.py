#!/usr/bin/env python3
"""
Test Chat Features - Demonstrates expertise elicitation and prompt comparison
"""

import requests
import time
import json

BASE_URL = "http://localhost:8000"

def test_chat_features():
    print("🧪 TESTING HUMANE-CHATBOT FEATURES")
    print("="*60)
    
    # Test 1: Start conversation
    print("\n1️⃣ Starting conversation...")
    response = requests.post(f"{BASE_URL}/conversation/start", 
                           json={"user_id": "test_user"})
    data = response.json()
    session_id = data['session_id']
    print(f"✅ Session started: {session_id}")
    
    # Test 2: Ask main question (should trigger expertise elicitation)
    print("\n2️⃣ Asking main question...")
    main_question = "What are the best AI models for computer vision?"
    print(f"👤 Question: {main_question}")
    
    payload = {
        "session_id": session_id,
        "message": main_question,
        "typing_start_time": int(time.time() * 1000) - 5000,
        "typing_end_time": int(time.time() * 1000) - 1000
    }
    
    response = requests.post(f"{BASE_URL}/conversation/message", json=payload)
    data = response.json()
    
    print(f"🤖 Bot response: {data['response']}")
    
    # Test 3: Answer expertise questions
    expertise_answers = [
        "I'm an expert in this field",
        "I want comprehensive details", 
        "I'm interested in practical applications"
    ]
    
    for i, answer in enumerate(expertise_answers, 1):
        print(f"\n3️⃣ Answering expertise question {i}...")
        print(f"👤 Answer: {answer}")
        
        payload = {
            "session_id": session_id,
            "message": answer,
            "typing_start_time": int(time.time() * 1000) - 5000,
            "typing_end_time": int(time.time() * 1000) - 1000
        }
        
        response = requests.post(f"{BASE_URL}/conversation/message", json=payload)
        data = response.json()
        
        if 'metadata' in data and 'expertise_elicitation' in data['metadata']:
            print(f"🤖 Bot: {data['response']}")
        else:
            print(f"🤖 Final response: {data['response']}")
            
            # Show prompt comparison
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
                print(f"\n📈 PERSONALIZATION PARAMETERS:")
                print(f"   Style: {params['response_style']}")
                print(f"   Detail: {params['detail_level']}")
                print(f"   Complexity: {params['language_complexity']}")
                print(f"   User Type: {params['user_type']}")
                print(f"   Engagement: {params['engagement_level']}")
    
    # Test 4: Ask a follow-up question
    print(f"\n4️⃣ Asking follow-up question...")
    follow_up = "Can you explain how these models work internally?"
    print(f"👤 Follow-up: {follow_up}")
    
    payload = {
        "session_id": session_id,
        "message": follow_up,
        "typing_start_time": int(time.time() * 1000) - 5000,
        "typing_end_time": int(time.time() * 1000) - 1000
    }
    
    response = requests.post(f"{BASE_URL}/conversation/message", json=payload)
    data = response.json()
    
    print(f"🤖 Response: {data['response']}")
    
    # Show prompt comparison for follow-up
    if 'metadata' in data and 'raw_prompt' in data['metadata']:
        print(f"\n📊 FOLLOW-UP PROMPT COMPARISON:")
        print(f"🔍 RAW: {data['metadata']['raw_prompt']}")
        print(f"🎯 TAILORED: {data['metadata']['tailored_prompt']}")
    
    print(f"\n✅ All tests completed successfully!")
    print("="*60)

if __name__ == "__main__":
    test_chat_features() 