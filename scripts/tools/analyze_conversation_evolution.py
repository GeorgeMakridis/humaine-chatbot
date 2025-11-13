#!/usr/bin/env python3
"""
Conversation Evolution Analysis

This script analyzes how the HumAIne-chatbot adapts over a conversation
and shows the metrics gathered during the interaction.
"""

import requests
import json
import time
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000"

def analyze_conversation_evolution():
    """Analyze conversation evolution with detailed metrics"""
    
    print("🔍 CONVERSATION EVOLUTION ANALYSIS")
    print("="*80)
    
    # Start a new conversation
    start_response = requests.post(f"{BASE_URL}/conversation/start", 
                                 json={"user_id": "evolution_analysis_user"})
    session_data = start_response.json()
    session_id = session_data['session_id']
    user_id = "evolution_analysis_user"
    
    print(f"✅ Started conversation: {session_id}")
    
    # Test conversation with different user behaviors
    test_messages = [
        # Initial technical question
        "Explain quantum computing in detail",
        
        # User shows confusion - wants simpler explanation
        "That's too complex. Can you explain it like I'm 5?",
        
        # User shows enthusiasm - wants more detail
        "Wow! This is amazing! Tell me everything about quantum algorithms!",
        
        # User shows frustration - wants conversational tone
        "I'm getting bored with all this technical stuff. Be more fun!",
        
        # User shows academic interest
        "Actually, I'm writing a research paper. Can you be more academic?",
        
        # User shows practical interest
        "What are the real-world applications?",
        
        # User shows emotional response
        "This is incredible! I'm so excited about this technology!",
        
        # User shows analytical thinking
        "What are the limitations and challenges?",
        
        # User shows casual interest
        "Cool! But can you summarize this in simple terms?",
        
        # Final request showing adaptation
        "Perfect! You really adapted to my style. Thanks!"
    ]
    
    # Track evolution
    evolution_data = []
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{'='*60}")
        print(f"TURN {i}: {message}")
        print(f"{'='*60}")
        
        # Send message
        payload = {
            "session_id": session_id,
            "message": message,
            "typing_start_time": int(time.time() * 1000) - 5000,
            "typing_end_time": int(time.time() * 1000) - 1000
        }
        
        response = requests.post(f"{BASE_URL}/conversation/message", json=payload)
        response_data = response.json()
        
        # Extract key metrics
        params = response_data['metadata']['personalization_params']
        context = response_data['metadata']['conversation_context']
        
        # Store evolution data
        evolution_data.append({
            'turn': i,
            'user_message': message,
            'response_preview': response_data['response'][:100] + "...",
            'personalization': params,
            'context': context
        })
        
        # Print analysis
        print(f"🤖 Response Style: {params['response_style']}")
        print(f"📊 Detail Level: {params['detail_level']}")
        print(f"🎯 Language Complexity: {params['language_complexity']}")
        print(f"👤 User Type: {params['user_type']}")
        print(f"💬 Engagement Level: {params['engagement_level']}")
        print(f"😊 Sentiment Preference: {params['sentiment_preference']}")
        print(f"📈 Total Turns: {context['total_turns']}")
        
        time.sleep(1)
    
    # Get final user profile
    print(f"\n{'='*80}")
    print("📊 FINAL USER PROFILE ANALYSIS")
    print(f"{'='*80}")
    
    profile_response = requests.get(f"{BASE_URL}/user/{user_id}/profile")
    final_profile = profile_response.json()
    
    print("🎯 User Profile Evolution:")
    print(f"  - User Type: {final_profile['profile']['personalization_params']['user_type']}")
    print(f"  - Preferred Style: {final_profile['profile']['profile_data']['preferred_response_style']}")
    print(f"  - Preferred Complexity: {final_profile['profile']['profile_data']['preferred_language_complexity']}")
    print(f"  - Preferred Detail Level: {final_profile['profile']['profile_data']['preferred_detail_level']}")
    
    # End conversation to get session metrics
    end_response = requests.post(f"{BASE_URL}/conversation/end", 
                               json={"session_id": session_id})
    session_metrics = end_response.json()
    
    print(f"\n📈 SESSION METRICS:")
    print(f"  - Session Duration: {session_metrics['session_data']['session_duration']}ms")
    print(f"  - Engagement Time: {session_metrics['session_data']['engagement']['engagement_time']}ms")
    print(f"  - Engagement Ratio: {session_metrics['session_data']['engagement']['engagement_time'] / session_metrics['session_data']['session_duration']:.2%}")
    print(f"  - Average Typing Speed: {session_metrics['session_data']['typing_speed']['average_typing_speed']} chars/sec")
    print(f"  - Language Complexity: {session_metrics['session_data']['language_complexity']['average_complexity_of_language']:.3f}")
    print(f"  - Sentiment Score: {session_metrics['session_data']['sentiment']['average_sentiment_score']}")
    
    # Analyze conversation evolution
    print(f"\n🔄 CONVERSATION EVOLUTION ANALYSIS:")
    print(f"{'='*80}")
    
    for i, data in enumerate(evolution_data):
        print(f"\nTurn {data['turn']}:")
        print(f"  User: {data['user_message']}")
        print(f"  Bot Style: {data['personalization']['response_style']}")
        print(f"  Detail Level: {data['personalization']['detail_level']}")
        print(f"  User Type: {data['personalization']['user_type']}")
        print(f"  Engagement: {data['personalization']['engagement_level']}")
    
    print(f"\n✅ Analysis completed!")
    print(f"Session ID: {session_id}")
    print(f"Total turns analyzed: {len(test_messages)}")

if __name__ == "__main__":
    analyze_conversation_evolution() 