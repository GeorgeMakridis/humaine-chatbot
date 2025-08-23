"""
Basic tests for HumAIne-chatbot

This module contains basic tests to verify the core functionality
of the HumAIne-chatbot system.
"""

import pytest
import time
from src.core.dialogue_manager import DialogueManager
from src.core.metrics_collector import MetricsCollector
from src.core.user_profiler import UserProfiler
from src.core.prompt_manager import PromptManager
from src.utils.sentiment_analyzer import SentimentAnalyzer
from src.utils.grammar_checker import GrammarChecker
from src.utils.language_complexity import LanguageComplexityAnalyzer


class TestMetricsCollector:
    """Test metrics collector functionality"""
    
    def test_start_session(self):
        """Test session start"""
        collector = MetricsCollector()
        user_id = "test_user_123"
        session_id = collector.start_session(user_id)
        
        assert session_id is not None
        assert session_id in collector.active_sessions
        assert collector.active_sessions[session_id]['user_id'] == user_id
    
    def test_record_user_message(self):
        """Test user message recording"""
        collector = MetricsCollector()
        user_id = "test_user_123"
        session_id = collector.start_session(user_id)
        
        message = "Hello, how are you?"
        start_time = int(time.time() * 1000)
        end_time = start_time + 5000  # 5 seconds later
        sent_time = end_time + 1000
        
        user_prompt = collector.record_user_message(
            session_id, message, start_time, end_time, sent_time
        )
        
        assert user_prompt.session_id == session_id
        assert user_prompt.user_id == user_id
        assert user_prompt.input_text == message
        assert user_prompt.typing_speed.typing_speed > 0
    
    def test_end_session(self):
        """Test session end"""
        collector = MetricsCollector()
        user_id = "test_user_123"
        session_id = collector.start_session(user_id)
        
        # Add some messages
        message = "Test message"
        start_time = int(time.time() * 1000)
        end_time = start_time + 2000
        sent_time = end_time + 500
        
        collector.record_user_message(session_id, message, start_time, end_time, sent_time)
        
        # End session
        session_data = collector.end_session(session_id)
        
        assert session_data is not None
        assert session_data.session_id == session_id
        assert session_data.user_id == user_id
        assert session_data.session_duration > 0


class TestUserProfiler:
    """Test user profiler functionality"""
    
    def test_create_user_profile(self):
        """Test user profile creation"""
        profiler = UserProfiler()
        user_id = "test_user_456"
        
        profile = profiler.create_user_profile(user_id)
        
        assert profile.user_id == user_id
        assert profile.total_sessions == 0
        assert profile.average_session_duration == 0
    
    def test_get_personalization_parameters(self):
        """Test personalization parameters retrieval"""
        profiler = UserProfiler()
        user_id = "test_user_456"
        
        # Create profile first
        profiler.create_user_profile(user_id)
        
        params = profiler.get_personalization_parameters(user_id)
        
        assert params is not None
        assert "language_complexity" in params
        assert "response_style" in params
        assert "detail_level" in params


class TestPromptManager:
    """Test prompt manager functionality"""
    
    def test_enrich_prompt(self):
        """Test prompt enrichment"""
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
        
        assert enriched_prompt is not None
        assert len(enriched_prompt) > len(base_prompt)
        assert "User: " in enriched_prompt
        assert "Assistant:" in enriched_prompt


class TestSentimentAnalyzer:
    """Test sentiment analyzer functionality"""
    
    def test_analyze_sentiment(self):
        """Test sentiment analysis"""
        analyzer = SentimentAnalyzer()
        
        # Test positive sentiment
        positive_text = "I love this chatbot! It's amazing and helpful."
        sentiment_score, normalized_score = analyzer.analyze_sentiment(positive_text)
        
        assert sentiment_score > 0
        assert normalized_score > 0
        
        # Test negative sentiment
        negative_text = "I hate this chatbot. It's terrible and useless."
        sentiment_score, normalized_score = analyzer.analyze_sentiment(negative_text)
        
        assert sentiment_score < 0
        assert normalized_score < 0


class TestGrammarChecker:
    """Test grammar checker functionality"""
    
    def test_analyze_grammar(self):
        """Test grammar analysis"""
        checker = GrammarChecker()
        
        # Test good grammar
        good_text = "This is a well-written sentence with proper grammar."
        total_words, mistakes, frequency = checker.analyze_grammar(good_text)
        
        assert total_words > 0
        assert frequency >= 0
        
        # Test poor grammar
        poor_text = "This sentence has bad grammar and spelling mistakes."
        total_words, mistakes, frequency = checker.analyze_grammar(poor_text)
        
        assert total_words > 0
        assert frequency >= 0


class TestLanguageComplexity:
    """Test language complexity analyzer"""
    
    def test_analyze_complexity(self):
        """Test language complexity analysis"""
        analyzer = LanguageComplexityAnalyzer()
        
        # Test simple text
        simple_text = "Hello world. This is simple."
        asl, ttr, complexity = analyzer.analyze_complexity(simple_text)
        
        assert asl >= 0
        assert 0 <= ttr <= 1
        assert 0 <= complexity <= 1
        
        # Test complex text
        complex_text = "The multifaceted nature of contemporary computational linguistics necessitates a comprehensive understanding of both theoretical frameworks and practical applications."
        asl, ttr, complexity = analyzer.analyze_complexity(complex_text)
        
        assert asl >= 0
        assert 0 <= ttr <= 1
        assert 0 <= complexity <= 1


class TestDialogueManager:
    """Test dialogue manager functionality"""
    
    def test_start_conversation(self):
        """Test conversation start"""
        manager = DialogueManager()
        user_id = "test_user_999"
        
        session_id = manager.start_conversation(user_id)
        
        assert session_id is not None
        assert session_id in manager.active_conversations
    
    def test_process_user_message(self):
        """Test user message processing"""
        manager = DialogueManager()
        user_id = "test_user_999"
        session_id = manager.start_conversation(user_id)
        
        message = "Hello, how are you?"
        start_time = int(time.time() * 1000)
        end_time = start_time + 3000
        
        response, metadata = manager.process_user_message(
            session_id, message, start_time, end_time
        )
        
        assert response is not None
        assert len(response) > 0
        assert metadata is not None
        assert "session_id" in metadata
        assert "user_id" in metadata


if __name__ == "__main__":
    # Run basic tests
    print("Running basic tests for HumAIne-chatbot...")
    
    # Test metrics collector
    test_collector = TestMetricsCollector()
    test_collector.test_start_session()
    test_collector.test_record_user_message()
    test_collector.test_end_session()
    
    # Test user profiler
    test_profiler = TestUserProfiler()
    test_profiler.test_create_user_profile()
    test_profiler.test_get_personalization_parameters()
    
    # Test prompt manager
    test_manager = TestPromptManager()
    test_manager.test_enrich_prompt()
    
    # Test utilities
    test_sentiment = TestSentimentAnalyzer()
    test_sentiment.test_analyze_sentiment()
    
    test_grammar = TestGrammarChecker()
    test_grammar.test_analyze_grammar()
    
    test_complexity = TestLanguageComplexity()
    test_complexity.test_analyze_complexity()
    
    # Test dialogue manager
    test_dialogue = TestDialogueManager()
    test_dialogue.test_start_conversation()
    test_dialogue.test_process_user_message()
    
    print("All basic tests passed!") 