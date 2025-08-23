"""
Demo script for HumAIne-chatbot

This script demonstrates the core functionality of the HumAIne-chatbot system,
showing how it personalizes responses based on user behavior and preferences.
"""

import time
import json
from datetime import datetime

from src.core.dialogue_manager import DialogueManager


def demo_basic_conversation():
    """Demonstrate basic conversation flow"""
    print("=" * 60)
    print("HUMANINE-CHATBOT DEMO")
    print("=" * 60)
    print()
    
    # Initialize dialogue manager
    dialogue_manager = DialogueManager()
    
    # Start conversation
    user_id = "demo_user_001"
    session_id = dialogue_manager.start_conversation(user_id)
    
    print(f"Started conversation for user: {user_id}")
    print(f"Session ID: {session_id}")
    print()
    
    # Sample conversation
    messages = [
        "Hello! I'm interested in learning about machine learning.",
        "Can you explain what neural networks are?",
        "What are some practical applications?",
        "How long does it take to learn the basics?"
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"User (Turn {i}): {message}")
        
        # Simulate typing time
        typing_start = int(time.time() * 1000)
        time.sleep(2)  # Simulate thinking/typing
        typing_end = int(time.time() * 1000)
        
        # Process message
        response, metadata = dialogue_manager.process_user_message(
            session_id, message, typing_start, typing_end
        )
        
        print(f"Bot: {response}")
        print(f"Personalization: {metadata['personalization_params']}")
        print()
        
        # Simulate feedback
        feedback_type = "positive" if i % 2 == 0 else "negative"
        dialogue_manager.record_feedback(
            session_id, response, typing_end, int(time.time() * 1000), feedback_type
        )
        
        time.sleep(1)  # Pause between turns
    
    # End conversation
    session_data = dialogue_manager.end_conversation(session_id, "taskCompletion")
    
    print("Conversation ended!")
    print(f"Session duration: {session_data.session_duration / 1000:.1f} seconds")
    print(f"Total turns: {session_data.feedback.total_bot_messages_count}")
    print(f"Feedback ratio: {session_data.feedback.total_feedback_ratio:.2%}")
    print()


def demo_user_profiling():
    """Demonstrate user profiling capabilities"""
    print("=" * 60)
    print("USER PROFILING DEMO")
    print("=" * 60)
    print()
    
    dialogue_manager = DialogueManager()
    
    # Create different user types
    user_types = [
        ("technical_expert", "Technical Expert"),
        ("casual_user", "Casual User"),
        ("professional_user", "Professional User"),
        ("student_user", "Student User")
    ]
    
    for user_id, user_name in user_types:
        print(f"Testing {user_name} profile...")
        
        # Create user profile
        profile = dialogue_manager.user_profiler.create_user_profile(user_id)
        
        # Get initial personalization parameters
        initial_params = dialogue_manager.get_personalization_parameters(user_id)
        
        print(f"  Initial parameters: {initial_params}")
        
        # Simulate a conversation to update profile
        session_id = dialogue_manager.start_conversation(user_id)
        
        # Send a test message
        message = "Can you explain artificial intelligence?"
        typing_start = int(time.time() * 1000)
        time.sleep(1)
        typing_end = int(time.time() * 1000)
        
        response, metadata = dialogue_manager.process_user_message(
            session_id, message, typing_start, typing_end
        )
        
        # Record feedback
        dialogue_manager.record_feedback(
            session_id, response, typing_end, int(time.time() * 1000), "positive"
        )
        
        # End session
        session_data = dialogue_manager.end_conversation(session_id, "taskCompletion")
        
        # Get updated parameters
        updated_params = dialogue_manager.get_personalization_parameters(user_id)
        
        print(f"  Updated parameters: {updated_params}")
        print(f"  Session duration: {session_data.session_duration / 1000:.1f}s")
        print(f"  Sentiment score: {session_data.sentiment.average_sentiment_score}")
        print()


def demo_metrics_collection():
    """Demonstrate metrics collection capabilities"""
    print("=" * 60)
    print("METRICS COLLECTION DEMO")
    print("=" * 60)
    print()
    
    dialogue_manager = DialogueManager()
    user_id = "metrics_demo_user"
    session_id = dialogue_manager.start_conversation(user_id)
    
    # Test different types of messages
    test_messages = [
        ("I love this chatbot! It's amazing and very helpful.", "positive"),
        ("This is terrible. I hate it.", "negative"),
        ("The weather is nice today.", "neutral"),
        ("Can you help me with my homework?", "question"),
        ("Thank you so much for your assistance!", "grateful")
    ]
    
    for i, (message, sentiment_type) in enumerate(test_messages, 1):
        print(f"Message {i}: {message}")
        print(f"Expected sentiment: {sentiment_type}")
        
        # Record message
        typing_start = int(time.time() * 1000)
        time.sleep(1.5)
        typing_end = int(time.time() * 1000)
        
        response, metadata = dialogue_manager.process_user_message(
            session_id, message, typing_start, typing_end
        )
        
        # Get metrics from the last recorded user prompt
        session_metrics = dialogue_manager.metrics_collector.session_metrics[session_id]
        if session_metrics:
            latest_metrics = session_metrics[-1]
            
            print(f"  Sentiment score: {latest_metrics['sentiment']['sentiment_score']}")
            print(f"  Language complexity: {latest_metrics['language_complexity']['complexity_of_language']:.2f}")
            print(f"  Grammar accuracy: {1 - latest_metrics['grammar']['grammatical_mistakes_frequency']:.2f}")
            print(f"  Typing speed: {latest_metrics['typing_speed']['typing_speed']:.1f} chars/sec")
            print()
        
        time.sleep(1)
    
    # End session and show aggregated metrics
    session_data = dialogue_manager.end_conversation(session_id, "taskCompletion")
    
    print("Session Summary:")
    print(f"  Average sentiment: {session_data.sentiment.average_sentiment_score}")
    print(f"  Average language complexity: {session_data.language_complexity.average_complexity_of_language:.2f}")
    print(f"  Average grammar accuracy: {1 - session_data.grammar.average_grammatical_mistakes_frequency:.2f}")
    print(f"  Average typing speed: {session_data.typing_speed.average_typing_speed:.1f} chars/sec")
    print(f"  Engagement ratio: {session_data.engagement.engagement_time / session_data.session_duration:.2%}")
    print()


def demo_prompt_enrichment():
    """Demonstrate prompt enrichment capabilities"""
    print("=" * 60)
    print("PROMPT ENRICHMENT DEMO")
    print("=" * 60)
    print()
    
    dialogue_manager = DialogueManager()
    prompt_manager = dialogue_manager.prompt_manager
    
    # Test different user types and their prompt enrichment
    test_cases = [
        {
            "user_type": "technical_expert",
            "message": "Explain quantum computing",
            "params": {
                "language_complexity": "complex",
                "response_style": "professional",
                "detail_level": "detailed",
                "user_type": "technical"
            }
        },
        {
            "user_type": "casual_user",
            "message": "What is AI?",
            "params": {
                "language_complexity": "simple",
                "response_style": "conversational",
                "detail_level": "concise",
                "user_type": "casual"
            }
        },
        {
            "user_type": "student_user",
            "message": "Help me understand machine learning",
            "params": {
                "language_complexity": "medium",
                "response_style": "enthusiastic",
                "detail_level": "detailed",
                "user_type": "educational"
            }
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"Case {i}: {case['user_type']}")
        print(f"Original message: {case['message']}")
        
        # Enrich prompt
        enriched_prompt = prompt_manager.enrich_prompt(
            case['message'], f"user_{i}", case['params']
        )
        
        print(f"Enriched prompt length: {len(enriched_prompt)} characters")
        print(f"Enrichment ratio: {len(enriched_prompt) / len(case['message']):.1f}x")
        print()
        
        # Show personalization context
        context = prompt_manager._create_personalization_context(case['params'])
        print(f"Personalization context: {context}")
        print("-" * 40)
        print()


def demo_user_study_simulation():
    """Demonstrate user study simulation"""
    print("=" * 60)
    print("USER STUDY SIMULATION DEMO")
    print("=" * 60)
    print()
    
    from user_study import UserStudySimulator
    
    simulator = UserStudySimulator()
    
    # Run a small simulation
    print("Running user study simulation with 5 participants...")
    results = simulator.simulate_user_study(num_participants=5)
    
    # Print summary
    simulator.print_study_summary(results)
    
    print("Simulation complete! Check data/user_sessions/ for detailed results.")


def main():
    """Run all demos"""
    print("Welcome to HumAIne-chatbot Demo!")
    print("This demo showcases the personalized conversational AI system.")
    print()
    
    try:
        # Run individual demos
        demo_basic_conversation()
        demo_user_profiling()
        demo_metrics_collection()
        demo_prompt_enrichment()
        demo_user_study_simulation()
        
        print("=" * 60)
        print("DEMO COMPLETE!")
        print("=" * 60)
        print()
        print("The HumAIne-chatbot system successfully demonstrates:")
        print("✓ Real-time user profiling and personalization")
        print("✓ Comprehensive metrics collection and analysis")
        print("✓ Dynamic prompt enrichment based on user preferences")
        print("✓ Reinforcement learning integration for continuous improvement")
        print("✓ User study framework for evaluation and validation")
        print()
        print("To run the full system:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Start the server: python main.py")
        print("3. Access the API at: http://localhost:8000")
        print("4. View API documentation at: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"Demo encountered an error: {e}")
        print("Please ensure all dependencies are installed and the system is properly configured.")


if __name__ == "__main__":
    main() 