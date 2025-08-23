#!/usr/bin/env python3
"""
Test Conversation Evolution Script

This script tests how the HumAIne-chatbot adapts over a conversation
with 10 follow-up prompts, tracking metrics and personalization changes.
"""

import requests
import json
import time
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000"

# Test conversation flow
CONVERSATION_FLOW = [
    "I want to learn about machine learning",
    "Can you explain supervised learning in more detail?",
    "What about neural networks? How do they work?",
    "I'm finding this quite technical. Can you simplify it?",
    "Actually, I prefer more detailed explanations. Give me the full technical breakdown.",
    "What are the real-world applications of deep learning?",
    "This is fascinating! Tell me more about AI ethics.",
    "I'm getting tired of all this text. Can you be more conversational?",
    "Thanks! But I need this for my research paper. Can you be more academic?",
    "Perfect! Now summarize everything we discussed in simple terms."
]

def send_message(session_id, message, turn_number):
    """Send a message and return the response with metadata"""
    payload = {
        "session_id": session_id,
        "message": message,
        "typing_start_time": int(time.time() * 1000) - 5000,
        "typing_end_time": int(time.time() * 1000) - 1000
    }
    
    response = requests.post(f"{BASE_URL}/conversation/message", json=payload)
    return response.json()

def get_user_profile(user_id):
    """Get the current user profile"""
    response = requests.get(f"{BASE_URL}/user/{user_id}/profile")
    return response.json()

def print_turn_analysis(turn_number, user_message, response_data):
    """Print analysis for each turn"""
    print(f"\n{'='*60}")
    print(f"TURN {turn_number}")
    print(f"{'='*60}")
    print(f"User Message: {user_message}")
    print(f"\nResponse: {response_data['response'][:200]}...")
    
    # Extract personalization parameters
    params = response_data['metadata']['personalization_params']
    print(f"\nPersonalization Parameters:")
    print(f"  - Language Complexity: {params['language_complexity']}")
    print(f"  - Response Style: {params['response_style']}")
    print(f"  - Detail Level: {params['detail_level']}")
    print(f"  - User Type: {params['user_type']}")
    print(f"  - Engagement Level: {params['engagement_level']}")
    print(f"  - Sentiment Preference: {params['sentiment_preference']}")
    
    # Extract conversation context
    context = response_data['metadata']['conversation_context']
    print(f"\nConversation Context:")
    print(f"  - Total Turns: {context['total_turns']}")
    print(f"  - User Messages: {context['user_messages']}")
    print(f"  - Assistant Messages: {context['assistant_messages']}")

def main():
    """Main test function"""
    print("🚀 Starting Conversation Evolution Test")
    print("="*60)
    
    # Start conversation
    start_response = requests.post(f"{BASE_URL}/conversation/start", 
                                 json={"user_id": "adaptive_test_user"})
    session_data = start_response.json()
    session_id = session_data['session_id']
    user_id = "adaptive_test_user"
    
    print(f"✅ Conversation started with session ID: {session_id}")
    
    # Get initial user profile
    print("\n📊 Initial User Profile:")
    initial_profile = get_user_profile(user_id)
    print(json.dumps(initial_profile, indent=2))
    
    # Send messages and track evolution
    for i, message in enumerate(CONVERSATION_FLOW, 1):
        print(f"\n🔄 Sending message {i}/{len(CONVERSATION_FLOW)}")
        
        # Send message
        response_data = send_message(session_id, message, i)
        
        # Print analysis
        print_turn_analysis(i, message, response_data)
        
        # Small delay between messages
        time.sleep(1)
    
    # Get final user profile
    print(f"\n{'='*60}")
    print("📊 FINAL USER PROFILE:")
    print(f"{'='*60}")
    final_profile = get_user_profile(user_id)
    print(json.dumps(final_profile, indent=2))
    
    # Get conversation analytics
    print(f"\n{'='*60}")
    print("📈 CONVERSATION ANALYTICS:")
    print(f"{'='*60}")
    
    # End conversation to get session data
    end_response = requests.post(f"{BASE_URL}/conversation/end", 
                               json={"session_id": session_id})
    session_data = end_response.json()
    print(json.dumps(session_data, indent=2))
    
    print(f"\n✅ Conversation evolution test completed!")
    print(f"Session ID: {session_id}")
    print(f"Total turns: {len(CONVERSATION_FLOW)}")

if __name__ == "__main__":
    main() 