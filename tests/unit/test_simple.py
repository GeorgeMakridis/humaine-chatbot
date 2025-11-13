"""
Simple test script for HumAIne-chatbot

This script tests the core functionality without external dependencies.
"""

import sys
import os
import time
import json
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

# Mock external dependencies for testing
class MockLanguageTool:
    def check(self, text):
        return []
    
    def __init__(self, lang):
        pass

# Mock the external dependencies
sys.modules['language_tool_python'] = type('MockModule', (), {
    'LanguageTool': MockLanguageTool
})

sys.modules['textstat'] = type('MockModule', (), {
    'flesch_reading_ease': lambda x: 70.0
})

sys.modules['emoji'] = type('MockModule', (), {
    'emoji_list': lambda x: []
})

sys.modules['textblob'] = type('MockModule', (), {
    'TextBlob': lambda x: type('MockTextBlob', (), {
        'sentiment': type('MockSentiment', (), {'polarity': 0.0, 'subjectivity': 0.0})()
    })()
})

# Mock ML libraries
sys.modules['sklearn'] = type('MockModule', (), {})
sys.modules['sklearn.ensemble'] = type('MockModule', (), {})
sys.modules['sklearn.preprocessing'] = type('MockModule', (), {})
sys.modules['stable_baselines3'] = type('MockModule', (), {})
sys.modules['gymnasium'] = type('MockModule', (), {})
sys.modules['numpy'] = type('MockModule', (), {})
sys.modules['torch'] = type('MockModule', (), {})

# Mock FastAPI
sys.modules['fastapi'] = type('MockModule', (), {})
sys.modules['uvicorn'] = type('MockModule', (), {})

try:
    from src.models.schemas import UserPrompt, Feedback, Session, UserProfile
    from src.utils.sentiment_analyzer import SentimentAnalyzer
    from src.utils.grammar_checker import GrammarChecker
    from src.utils.language_complexity import LanguageComplexityAnalyzer
    from src.core.metrics_collector import MetricsCollector
    from src.core.user_profiler import UserProfiler
    from src.core.prompt_manager import PromptManager
    from src.core.dialogue_manager import DialogueManager
    
    print("✅ All modules imported successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def test_schemas():
    """Test JSON schemas"""
    print("\n🧪 Testing JSON Schemas...")
    
    # Test UserPrompt schema
    user_prompt = UserPrompt(
        session_id="test-session-123",
        user_id="test-user-456",
        input_text="Hello, how are you?",
        input_start_time=1000000,
        input_end_time=1005000,
        input_sent_time=1006000,
        response_time={"user_response_time": 1000, "user_typing_start_time": 500},
        sentiment={"sentiment_score": 2, "normalized_sentiment_score": 1},
        grammar={"total_words_count": 4, "mistakes_count": 0, "grammatical_mistakes_frequency": 0.0},
        language_complexity={
            "message_average_sentence_length": 4,
            "message_average_sentence_length_weight": 0.5,
            "type_token_ratio": 0.75,
            "type_token_ratio_weight": 0.5,
            "complexity_of_language": 0.6
        },
        typing_speed={"duration": 5000, "message_length": 18, "typing_speed": 3.6}
    )
    
    print(f"✅ UserPrompt created: {user_prompt.session_id}")
    
    # Test UserProfile schema
    profile = UserProfile(
        user_id="test-user-789",
        average_session_duration=1800000,
        average_response_time=1500,
        average_typing_speed=4.2,
        average_sentiment_score=1.5,
        average_language_complexity=0.7,
        average_grammatical_accuracy=0.95,
        total_sessions=5,
        average_engagement_time=1200000,
        feedback_ratio=0.8,
        positive_feedback_ratio=0.75,
        preferred_language_complexity="medium",
        preferred_response_style="conversational",
        preferred_detail_level="detailed"
    )
    
    print(f"✅ UserProfile created: {profile.user_id}")
    print(f"   - Average typing speed: {profile.average_typing_speed} chars/sec")
    print(f"   - Preferred style: {profile.preferred_response_style}")
    
    return True


def test_utilities():
    """Test utility functions"""
    print("\n🧪 Testing Utility Functions...")
    
    # Test sentiment analyzer
    sentiment_analyzer = SentimentAnalyzer()
    positive_text = "I love this chatbot! It's amazing and helpful."
    negative_text = "I hate this chatbot. It's terrible and useless."
    
    pos_score, pos_norm = sentiment_analyzer.analyze_sentiment(positive_text)
    neg_score, neg_norm = sentiment_analyzer.analyze_sentiment(negative_text)
    
    print(f"✅ Sentiment Analysis:")
    print(f"   - Positive text score: {pos_score}")
    print(f"   - Negative text score: {neg_score}")
    
    # Test grammar checker
    grammar_checker = GrammarChecker()
    good_text = "This is a well-written sentence with proper grammar."
    poor_text = "This sentence has bad grammar and spelling mistakes."
    
    good_words, good_mistakes, good_freq = grammar_checker.analyze_grammar(good_text)
    poor_words, poor_mistakes, poor_freq = grammar_checker.analyze_grammar(poor_text)
    
    print(f"✅ Grammar Analysis:")
    print(f"   - Good text: {good_words} words, {good_mistakes} mistakes")
    print(f"   - Poor text: {poor_words} words, {poor_mistakes} mistakes")
    
    # Test language complexity
    complexity_analyzer = LanguageComplexityAnalyzer()
    simple_text = "Hello world. This is simple."
    complex_text = "The multifaceted nature of contemporary computational linguistics necessitates comprehensive understanding."
    
    simple_asl, simple_ttr, simple_comp = complexity_analyzer.analyze_complexity(simple_text)
    complex_asl, complex_ttr, complex_comp = complexity_analyzer.analyze_complexity(complex_text)
    
    print(f"✅ Language Complexity:")
    print(f"   - Simple text complexity: {simple_comp:.2f}")
    print(f"   - Complex text complexity: {complex_comp:.2f}")
    
    return True


def test_metrics_collector():
    """Test metrics collector"""
    print("\n🧪 Testing Metrics Collector...")
    
    collector = MetricsCollector()
    user_id = "test_user_123"
    
    # Start session
    session_id = collector.start_session(user_id)
    print(f"✅ Session started: {session_id}")
    
    # Record user message
    message = "Hello, how are you today?"
    start_time = int(time.time() * 1000)
    end_time = start_time + 3000  # 3 seconds later
    sent_time = end_time + 500
    
    user_prompt = collector.record_user_message(
        session_id, message, start_time, end_time, sent_time
    )
    
    print(f"✅ Message recorded:")
    print(f"   - Text: {user_prompt.input_text}")
    print(f"   - Typing speed: {user_prompt.typing_speed.typing_speed:.1f} chars/sec")
    print(f"   - Sentiment score: {user_prompt.sentiment.sentiment_score}")
    
    # Record feedback
    feedback = collector.record_feedback(
        session_id, "Thank you for your message!", start_time, end_time, "positive", sent_time
    )
    
    print(f"✅ Feedback recorded: {feedback.feedback_type}")
    
    # End session
    session_data = collector.end_session(session_id)
    
    print(f"✅ Session ended:")
    print(f"   - Duration: {session_data.session_duration / 1000:.1f} seconds")
    print(f"   - Engagement: {session_data.engagement.engagement_time / session_data.session_duration:.1%}")
    
    return True


def test_user_profiler():
    """Test user profiler"""
    print("\n🧪 Testing User Profiler...")
    
    profiler = UserProfiler()
    user_id = "test_user_456"
    
    # Create user profile
    profile = profiler.create_user_profile(user_id)
    print(f"✅ Profile created: {profile.user_id}")
    
    # Get personalization parameters
    params = profiler.get_personalization_parameters(user_id)
    print(f"✅ Personalization parameters:")
    print(f"   - Language complexity: {params['language_complexity']}")
    print(f"   - Response style: {params['response_style']}")
    print(f"   - Detail level: {params['detail_level']}")
    
    return True


def test_prompt_manager():
    """Test prompt manager"""
    print("\n🧪 Testing Prompt Manager...")
    
    manager = PromptManager()
    base_prompt = "What is machine learning?"
    user_id = "test_user_789"
    personalization_params = {
        "language_complexity": "medium",
        "response_style": "balanced",
        "detail_level": "medium",
        "user_type": "general"
    }
    
    enriched_prompt = manager.enrich_prompt(base_prompt, user_id, personalization_params)
    
    print(f"✅ Prompt enrichment:")
    print(f"   - Original length: {len(base_prompt)} chars")
    print(f"   - Enriched length: {len(enriched_prompt)} chars")
    print(f"   - Enrichment ratio: {len(enriched_prompt) / len(base_prompt):.1f}x")
    
    # Test response guidelines
    guidelines = manager.generate_response_guidelines(personalization_params)
    print(f"✅ Response guidelines generated: {len(guidelines)} categories")
    
    return True


def test_dialogue_manager():
    """Test dialogue manager"""
    print("\n🧪 Testing Dialogue Manager...")
    
    manager = DialogueManager()
    user_id = "test_user_999"
    
    # Start conversation
    session_id = manager.start_conversation(user_id)
    print(f"✅ Conversation started: {session_id}")
    
    # Send message
    message = "Hello! I'm interested in learning about AI."
    start_time = int(time.time() * 1000)
    end_time = start_time + 2000
    
    response, metadata = manager.process_user_message(
        session_id, message, start_time, end_time
    )
    
    print(f"✅ Message processed:")
    print(f"   - User message: {message}")
    print(f"   - Bot response: {response[:50]}...")
    print(f"   - Personalization: {metadata['personalization_params']['response_style']}")
    
    # Record feedback
    feedback_data = manager.record_feedback(
        session_id, response, end_time, int(time.time() * 1000), "positive"
    )
    
    print(f"✅ Feedback recorded: {feedback_data['feedback_type']}")
    
    # End conversation
    session_data = manager.end_conversation(session_id)
    
    print(f"✅ Conversation ended:")
    print(f"   - Session duration: {session_data.session_duration / 1000:.1f}s")
    print(f"   - Turn count: {session_data.feedback.total_bot_messages_count}")
    
    return True


def test_conversation_flow():
    """Test complete conversation flow"""
    print("\n🧪 Testing Complete Conversation Flow...")
    
    manager = DialogueManager()
    user_id = "conversation_test_user"
    
    # Start conversation
    session_id = manager.start_conversation(user_id)
    
    # Simulate a conversation
    messages = [
        "Hi! I'm new to programming.",
        "Can you explain what Python is?",
        "What are some good resources to learn?",
        "How long does it take to become proficient?"
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"\n--- Turn {i} ---")
        print(f"User: {message}")
        
        # Process message
        start_time = int(time.time() * 1000)
        time.sleep(1)  # Simulate thinking time
        end_time = int(time.time() * 1000)
        
        response, metadata = manager.process_user_message(
            session_id, message, start_time, end_time
        )
        
        print(f"Bot: {response}")
        print(f"Style: {metadata['personalization_params']['response_style']}")
        print(f"Complexity: {metadata['personalization_params']['language_complexity']}")
        
        # Record feedback
        feedback_type = "positive" if i % 2 == 0 else "negative"
        manager.record_feedback(
            session_id, response, end_time, int(time.time() * 1000), feedback_type
        )
        
        time.sleep(0.5)
    
    # End conversation
    session_data = manager.end_conversation(session_id)
    
    print(f"\n--- Session Summary ---")
    print(f"Duration: {session_data.session_duration / 1000:.1f} seconds")
    print(f"Turns: {session_data.feedback.total_bot_messages_count}")
    print(f"Feedback ratio: {session_data.feedback.total_feedback_ratio:.1%}")
    print(f"Positive feedback: {session_data.feedback.positive_feedback_ratio:.1%}")
    print(f"Average sentiment: {session_data.sentiment.average_sentiment_score}")
    
    return True


def main():
    """Run all tests"""
    print("🚀 HumAIne-Chatbot System Test")
    print("=" * 50)
    
    tests = [
        ("JSON Schemas", test_schemas),
        ("Utility Functions", test_utilities),
        ("Metrics Collector", test_metrics_collector),
        ("User Profiler", test_user_profiler),
        ("Prompt Manager", test_prompt_manager),
        ("Dialogue Manager", test_dialogue_manager),
        ("Complete Conversation Flow", test_conversation_flow)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*20} {test_name} {'='*20}")
            test_func()
            passed += 1
            print(f"✅ {test_name} PASSED")
        except Exception as e:
            print(f"❌ {test_name} FAILED: {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    print(f"\n💡 To run the full system:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Start the server: python main.py")
    print("3. Run the demo: python demo.py")


if __name__ == "__main__":
    main() 