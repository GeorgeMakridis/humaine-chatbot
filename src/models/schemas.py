"""
JSON Schemas for User Profiling and Personalization

This module contains the JSON schemas used in the HumAIne-chatbot system
for collecting and organizing metrics related to user interactions,
personalization, and feedback.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class ResponseTime(BaseModel):
    """User Response Time metrics"""
    user_response_time: int = Field(description="Time (ms) taken by the user to respond after receiving a chatbot message")
    user_typing_start_time: int = Field(description="Time (ms) taken by the user to start typing their response after receiving a bot message")


class Sentiment(BaseModel):
    """Sentiment Score Analysis"""
    sentiment_score: int = Field(ge=-5, le=5, description="Emotional score of the user message (-5 to +5)")
    normalized_sentiment_score: int = Field(ge=-5, le=5, description="Normalized sentiment score relative to message length")


class Grammar(BaseModel):
    """Grammar Analysis"""
    total_words_count: int = Field(description="Total number of words in the user's message")
    mistakes_count: int = Field(description="Total number of grammatical mistakes identified in the user's message")
    grammatical_mistakes_frequency: float = Field(ge=0, le=1, description="Frequency of grammatical mistakes in the user's message")


class LanguageComplexity(BaseModel):
    """Complexity of Language"""
    message_average_sentence_length: int = Field(description="Average length of sentences in the user's message")
    message_average_sentence_length_weight: float = Field(ge=0, le=1, description="Weight for average sentence length")
    type_token_ratio: float = Field(ge=0, le=1, description="Ratio of unique words to total words in the user's message")
    type_token_ratio_weight: float = Field(ge=0, le=1, description="Weight for type-token ratio")
    complexity_of_language: float = Field(description="Composite score reflecting overall language complexity")


class TypingSpeed(BaseModel):
    """Typing Speed Analysis"""
    duration: int = Field(description="Total time (ms) it takes for the user to type and send their message")
    message_length: int = Field(description="Total number of characters in the user's message")
    typing_speed: float = Field(description="Speed (characters per second) at which the user types")


class UserPrompt(BaseModel):
    """User Prompt Schema - captures detailed information about each user message"""
    session_id: str = Field(description="Unique session identifier (Version 4 UUID)")
    user_id: str = Field(description="Unique user identifier (Version 4 UUID)")
    input_text: str = Field(description="Text of the prompt")
    input_start_time: int = Field(description="Unix timestamp (ms) when the user began typing the prompt")
    input_end_time: int = Field(description="Unix timestamp (ms) when the user finished typing the prompt")
    input_sent_time: int = Field(description="Unix timestamp (ms) when the message was sent")
    response_time: ResponseTime
    sentiment: Sentiment
    grammar: Grammar
    language_complexity: LanguageComplexity
    typing_speed: TypingSpeed

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "d5d539b8-cc6c-48e9-9454-ff1c69933ec8",
                "user_id": "2b5516f1-df98-4408-8640-ba156e7d0197",
                "input_text": "How are you doing today?",
                "input_start_time": 1737365162000,
                "input_end_time": 1737365168000,
                "input_sent_time": 1737365170000,
                "response_time": {
                    "user_response_time": 1200,
                    "user_typing_start_time": 500
                },
                "sentiment": {
                    "sentiment_score": 2,
                    "normalized_sentiment_score": 1
                },
                "grammar": {
                    "total_words_count": 5,
                    "mistakes_count": 0,
                    "grammatical_mistakes_frequency": 0
                },
                "language_complexity": {
                    "message_average_sentence_length": 6,
                    "message_average_sentence_length_weight": 0.5,
                    "type_token_ratio": 0.8,
                    "type_token_ratio_weight": 0.5,
                    "complexity_of_language": 0.7
                },
                "typing_speed": {
                    "duration": 5000,
                    "message_length": 24,
                    "typing_speed": 4.8
                }
            }
        }


class UserPromptSimple(BaseModel):
    """Simplified User Prompt Schema - matches exactly what the UI sends"""
    session_id: str = Field(description="Unique session identifier")
    user_id: str = Field(description="Unique user identifier")
    input_text: str = Field(description="Text of the prompt")
    input_start_time: int = Field(description="Unix timestamp (ms) when the user began typing the prompt")
    input_end_time: int = Field(description="Unix timestamp (ms) when the user finished typing the prompt")
    input_sent_time: int = Field(description="Unix timestamp (ms) when the message was sent")
    
    # Additional metrics from userMessage.metrics may be included dynamically
    # These are optional and not required by the schema

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "test_session_123",
                "user_id": "test_user_456",
                "input_text": "Hello, how are you today?",
                "input_start_time": 1737365162000,
                "input_end_time": 1737365168000,
                "input_sent_time": 1737365170000
            }
        }


class Feedback(BaseModel):
    """Feedback Schema - tracks user feedback on chatbot responses"""
    session_id: str = Field(description="Unique session identifier (Version 4 UUID)")
    user_id: str = Field(description="Unique user identifier (Version 4 UUID)")
    response_text: str = Field(description="The text content of the bot's response to the user")
    response_start_time: int = Field(description="The timestamp (in Unix format) when the request for the response was made")
    response_end_time: int = Field(description="The timestamp (in Unix format) when the bot's response was received by the user")
    response_duration: int = Field(description="The duration (in milliseconds) it took for the bot's response to be delivered")
    feedback_type: str = Field(description="The type of feedback the user provided", pattern="^(positive|negative)$")
    feedback_time: int = Field(description="The timestamp (in Unix format) when the user submitted the feedback")
    feedback_delay_duration: int = Field(description="The duration (in milliseconds) between the bot's message being delivered and the user submitting feedback")

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "d5d539b8-cc6c-48e9-9454-ff1c69933ec8",
                "user_id": "2b5516f1-df98-4408-8640-ba156e7d0197",
                "response_text": "Thank you for your input! Please rate your experience.",
                "response_start_time": 1619112399000,
                "response_end_time": 1619112401000,
                "response_duration": 2000,
                "feedback_type": "positive",
                "feedback_time": 1619112450000,
                "feedback_delay_duration": 4000
            }
        }


class Engagement(BaseModel):
    """Engagement metrics for a session"""
    idle_time: int = Field(description="Total time (ms) during the session when the user was inactive")
    active_time: int = Field(description="Total time (ms) during the session when the user was active")
    engagement_time: int = Field(description="Total time (ms) spent interacting during the session")


class FeedbackData(BaseModel):
    """Feedback Data aggregated for a session"""
    total_feedback_count: int = Field(description="Total number of feedback instances provided by the user")
    total_bot_messages_count: int = Field(description="Total number of messages sent by the chatbot during the session")
    total_feedback_ratio: float = Field(ge=0, le=1, description="Ratio of feedback messages to total bot messages")
    positive_feedback_count: int = Field(description="Total number of bot messages that received positive feedback")
    positive_feedback_ratio: float = Field(ge=0, le=1, description="Ratio of bot messages that received positive feedback")
    negative_feedback_count: int = Field(description="Total number of bot messages that received negative feedback")
    negative_feedback_ratio: float = Field(ge=0, le=1, description="Ratio of bot messages that received negative feedback")
    positive_follow_up_count: int = Field(description="Number of instances where negative feedback was followed by positive feedback")
    feedback_incorporation_rate: float = Field(ge=0, le=1, description="Proportion of negative feedback instances followed by positive feedback")


class SessionResponseTime(BaseModel):
    """Average response time metrics for a session"""
    average_user_response_time: float = Field(description="Average time (ms) taken by users to respond to chatbot messages")
    average_user_typing_start_time: float = Field(description="Average time (ms) taken by the user to start typing their response")


class SessionSentiment(BaseModel):
    """Average sentiment metrics for a session"""
    average_sentiment_score: int = Field(ge=-5, le=5, description="Average sentiment score across a session")
    average_normalized_sentiment_score: int = Field(ge=-5, le=5, description="Average normalized sentiment score across sessions")


class SessionGrammar(BaseModel):
    """Average grammar metrics for a session"""
    average_total_words_count: float = Field(description="Average number of words in the user messages across a session")
    average_mistakes_count: float = Field(description="Average number of grammatical mistakes in user messages across a session")
    average_grammatical_mistakes_frequency: float = Field(description="Average grammatical mistakes frequency in user messages across a session")


class SessionLanguageComplexity(BaseModel):
    """Average language complexity metrics for a session"""
    average_message_average_sentence_length: float = Field(description="Average sentence length of the user's messages across all messages in a session")
    average_type_token_ratio: float = Field(description="Average type-token ratio of unique words in the user's messages across all messages in a session")
    average_complexity_of_language: float = Field(description="Average complexity of the user's language across all messages in a session")


class SessionTypingSpeed(BaseModel):
    """Average typing speed metrics for a session"""
    average_duration: float = Field(description="Mean duration across all messages in the session")
    average_message_length: float = Field(description="Mean message length across all messages in the session")
    average_typing_speed: float = Field(description="Mean typing speed across all messages in the session")


class Session(BaseModel):
    """Session Schema - aggregates metrics across an entire conversation session"""
    session_id: str = Field(description="Unique session identifier (Version 4 UUID)")
    user_id: str = Field(description="Unique user identifier (Version 4 UUID)")
    session_start: int = Field(description="Unix timestamp (ms) when the session starts")
    session_end: int = Field(description="Unix timestamp (ms) when the session ends")
    session_end_type: str = Field(description="Reason for session termination", pattern="^(userAction|inactivity|taskCompletion)$")
    session_duration: int = Field(description="Session duration (ms) calculated as session_end - session_start")
    engagement: Engagement
    feedback: FeedbackData
    response_time: SessionResponseTime
    sentiment: SessionSentiment
    grammar: SessionGrammar
    language_complexity: SessionLanguageComplexity
    typing_speed: SessionTypingSpeed

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "d5d539b8-cc6c-48e9-9454-ff1c69933ec8",
                "user_id": "2b5516f1-df98-4408-8640-ba156e7d0197",
                "session_start": 1737365162000,
                "session_end": 1737368762000,
                "session_end_type": "taskCompletion",
                "session_duration": 3600000,
                "engagement": {
                    "idle_time": 5000,
                    "active_time": 15000,
                    "engagement_time": 20000
                },
                "feedback": {
                    "total_feedback_count": 5,
                    "total_bot_messages_count": 10,
                    "total_feedback_ratio": 0.5,
                    "positive_feedback_count": 3,
                    "positive_feedback_ratio": 0.6,
                    "negative_feedback_count": 2,
                    "negative_feedback_ratio": 0.4,
                    "positive_follow_up_count": 1,
                    "feedback_incorporation_rate": 0.8
                },
                "response_time": {
                    "average_user_response_time": 1200,
                    "average_user_typing_start_time": 500
                },
                "sentiment": {
                    "average_sentiment_score": 2,
                    "average_normalized_sentiment_score": 3
                },
                "grammar": {
                    "average_total_words_count": 350,
                    "average_mistakes_count": 2,
                    "average_grammatical_mistakes_frequency": 0.06
                },
                "language_complexity": {
                    "average_message_average_sentence_length": 15,
                    "average_type_token_ratio": 0.85,
                    "average_complexity_of_language": 0.75
                },
                "typing_speed": {
                    "average_duration": 5000,
                    "average_message_length": 24,
                    "average_typing_speed": 4.8
                }
            }
        }


class UserProfile(BaseModel):
    """User Profile - comprehensive user characterization"""
    user_id: str = Field(description="Unique user identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Behavioral metrics
    average_session_duration: float = Field(default=0, description="Average session duration in milliseconds")
    average_response_time: float = Field(default=0, description="Average response time in milliseconds")
    average_typing_speed: float = Field(default=0, description="Average typing speed in characters per second")
    
    # Linguistic metrics
    average_sentiment_score: float = Field(default=0, description="Average sentiment score (-5 to +5)")
    average_language_complexity: float = Field(default=0, description="Average language complexity score")
    average_grammatical_accuracy: float = Field(default=1, description="Average grammatical accuracy (0 to 1)")
    
    # Engagement metrics
    total_sessions: int = Field(default=0, description="Total number of sessions")
    average_engagement_time: float = Field(default=0, description="Average engagement time per session")
    feedback_ratio: float = Field(default=0, description="Ratio of sessions with feedback")
    positive_feedback_ratio: float = Field(default=0, description="Ratio of positive feedback")
    
    # Personalization preferences
    preferred_language_complexity: str = Field(default="medium", description="Preferred language complexity level")
    preferred_response_style: str = Field(default="balanced", description="Preferred response style")
    preferred_detail_level: str = Field(default="medium", description="Preferred detail level")
    
    # Session and feedback history
    session_history: List[Dict[str, Any]] = Field(default_factory=list, description="History of user sessions")
    feedback_history: List[Dict[str, Any]] = Field(default_factory=list, description="History of user feedback")
    
    # Cross-session insights
    cross_session_insights: Dict[str, Any] = Field(default_factory=dict, description="Insights from cross-session analysis")
    
    # RL agent state
    rl_state: Dict[str, Any] = Field(default_factory=dict, description="Reinforcement learning agent state")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "2b5516f1-df98-4408-8640-ba156e7d0197",
                "average_session_duration": 1800000,
                "average_response_time": 1500,
                "average_typing_speed": 4.2,
                "average_sentiment_score": 1.5,
                "average_language_complexity": 0.7,
                "average_grammatical_accuracy": 0.95,
                "total_sessions": 5,
                "average_engagement_time": 1200000,
                "feedback_ratio": 0.8,
                "positive_feedback_ratio": 0.75,
                "preferred_language_complexity": "medium",
                "preferred_response_style": "conversational",
                "preferred_detail_level": "detailed"
            }
        } 