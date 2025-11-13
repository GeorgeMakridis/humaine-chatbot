#!/usr/bin/env python3
"""
Demo: Different Expertise Levels
"""

import requests
import time

BASE_URL = "http://localhost:8000"

def demo_beginner_user():
    print("🎓 DEMO: Beginner User Experience")
    print("="*60)
    
    # Start conversation
    response = requests.post(f"{BASE_URL}/conversation/start", 
                           json={"user_id": "beginner_demo"})
    data = response.json()
    session_id = data['session_id']
    
    # Ask main question
    main_question = "What is machine learning?"
    print(f"\n👤 Beginner asks: {main_question}")
    
    payload = {
        "session_id": session_id,
        "message": main_question,
        "typing_start_time": int(time.time() * 1000) - 5000,
        "typing_end_time": int(time.time() * 1000) - 1000
    }
    
    response = requests.post(f"{BASE_URL}/conversation/message", json=payload)
    data = response.json()
    print(f"\n🤖 Bot: {data['response']}")
    
    # Answer expertise questions as beginner
    beginner_answers = [
        "I'm a beginner",
        "I want simple explanations",
        "I'm interested in basic concepts"
    ]
    
    for i, answer in enumerate(beginner_answers, 1):
        print(f"\n👤 Beginner answers: {answer}")
        
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
            print(f"\n🤖 Bot: {data['response']}")
            
            # Show personalization
            if 'metadata' in data and 'personalization_params' in data['metadata']:
                params = data['metadata']['personalization_params']
                print(f"\n📈 PERSONALIZATION FOR BEGINNER:")
                print(f"   Style: {params['response_style']}")
                print(f"   Detail: {params['detail_level']}")
                print(f"   Complexity: {params['language_complexity']}")
    
    print(f"\n✅ Beginner demo completed!")
    print("="*60)

def demo_expert_user():
    print("\n🎓 DEMO: Expert User Experience")
    print("="*60)
    
    # Start conversation
    response = requests.post(f"{BASE_URL}/conversation/start", 
                           json={"user_id": "expert_demo"})
    data = response.json()
    session_id = data['session_id']
    
    # Ask main question
    main_question = "Explain the mathematical foundations of transformer architectures"
    print(f"\n👤 Expert asks: {main_question}")
    
    payload = {
        "session_id": session_id,
        "message": main_question,
        "typing_start_time": int(time.time() * 1000) - 5000,
        "typing_end_time": int(time.time() * 1000) - 1000
    }
    
    response = requests.post(f"{BASE_URL}/conversation/message", json=payload)
    data = response.json()
    print(f"\n🤖 Bot: {data['response']}")
    
    # Answer expertise questions as expert
    expert_answers = [
        "I'm an expert",
        "I want comprehensive details",
        "I'm interested in theoretical concepts"
    ]
    
    for i, answer in enumerate(expert_answers, 1):
        print(f"\n👤 Expert answers: {answer}")
        
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
            print(f"\n🤖 Bot: {data['response']}")
            
            # Show personalization
            if 'metadata' in data and 'personalization_params' in data['metadata']:
                params = data['metadata']['personalization_params']
                print(f"\n📈 PERSONALIZATION FOR EXPERT:")
                print(f"   Style: {params['response_style']}")
                print(f"   Detail: {params['detail_level']}")
                print(f"   Complexity: {params['language_complexity']}")
    
    print(f"\n✅ Expert demo completed!")
    print("="*60)

def main():
    demo_beginner_user()
    demo_expert_user()
    print("\n🎉 Both demos completed! Notice the difference in personalization!")

if __name__ == "__main__":
    main() 