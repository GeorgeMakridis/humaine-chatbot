#!/usr/bin/env python3
"""
Test script for OpenAI API integration

This script tests the OpenAI API connectivity and response generation.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.core.openai_integration import OpenAIIntegration

def test_openai_integration():
    """Test OpenAI integration"""
    print("🧪 Testing OpenAI Integration")
    print("=" * 40)
    
    # Check if API key is loaded
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No OPENAI_API_KEY found in environment")
        return False
    
    print(f"✅ API Key loaded: {api_key[:20]}...")
    
    # Initialize OpenAI integration
    try:
        openai_integration = OpenAIIntegration()
        print("✅ OpenAI integration initialized")
    except Exception as e:
        print(f"❌ Failed to initialize OpenAI integration: {e}")
        return False
    
    # Check connectivity
    print("\n🔍 Checking OpenAI connectivity...")
    connectivity = openai_integration.check_connectivity()
    
    if connectivity['status'] == 'connected':
        print("✅ OpenAI API connected successfully!")
        print(f"   Model: {connectivity.get('model', 'N/A')}")
        print(f"   Test response: {connectivity.get('test_response', 'N/A')}")
    else:
        print(f"❌ OpenAI API connection failed: {connectivity}")
        return False
    
    # Test response generation
    print("\n💬 Testing response generation...")
    test_message = "Hello! How are you today?"
    personalization = {
        'language_complexity': 'medium',
        'response_style': 'conversational',
        'detail_level': 'balanced'
    }
    
    try:
        response = openai_integration.generate_response(
            test_message, 
            personalization
        )
        print(f"✅ Response generated: {response[:100]}...")
    except Exception as e:
        print(f"❌ Response generation failed: {e}")
        return False
    
    print("\n🎉 All tests passed! OpenAI integration is working correctly.")
    return True

if __name__ == "__main__":
    success = test_openai_integration()
    sys.exit(0 if success else 1)
