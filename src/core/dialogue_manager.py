"""
Dialogue Manager for HumAIne-chatbot

This module manages the overall conversation flow, coordinating between
the user interface, metrics collection, user profiling, and prompt management.
"""

import asyncio
from typing import Dict, Any, Optional, List
import numpy as np
from datetime import datetime

from ..models.schemas import UserProfile, Session
from ..core.user_profiler import UserProfiler
from ..core.metrics_collector import MetricsCollector
from ..core.openai_integration import OpenAIIntegration

class DialogueManager:
    def __init__(self, user_profiler: UserProfiler, metrics_collector: MetricsCollector, openai_integration: OpenAIIntegration):
        self.user_profiler = user_profiler
        self.metrics_collector = metrics_collector
        self.openai_integration = openai_integration
        self.active_conversations: Dict[str, Dict[str, Any]] = {}
        self.rl_agents = {}

    async def process_user_input(self, prompt_data: Dict[str, Any]) -> str:
        """Process user input and return chatbot response - handles exact UI data structure"""
        try:
            # Extract data - preserving ALL original fields
            session_id = prompt_data["session_id"]
            user_id = prompt_data["user_id"]
            input_text = prompt_data["input_text"]
            
            # Record ALL metrics from the UI (including userMessage.metrics)
            self.metrics_collector.record_user_prompt(prompt_data)
            
            # Update user profile with ALL the data
            self.user_profiler.update_profile_from_prompt(prompt_data)
            
            # Get user profile
            user_profile = self.user_profiler.get_user_profile(user_id)
            
            # Initialize RL agent if needed (disabled for now to prefer OpenAI)
            # if user_id not in self.rl_agents:
            #     try:
            #         from ..models.rl_agent import ChatbotRLAgent
            #         self.rl_agents[user_id] = ChatbotRLAgent(user_profile)
            #         print(f"✅ Initialized RL agent for user {user_id}")
            #     except Exception as e:
            #         print(f"⚠️  Failed to initialize RL agent: {e}")
            #         self.rl_agents[user_id] = None
            
            # Generate response
            # Use OpenAI integration for real responses
            try:
                # Extract personalization parameters from user profile
                personalization_params = {
                    "temperature": 0.7,  # Default value since UserProfile doesn't have this
                    "max_tokens": 1000,  # Default value since UserProfile doesn't have this
                    "detail_level": getattr(user_profile, 'preferred_detail_level', 'medium'),
                    "expertise_level": "beginner",  # Default value since UserProfile doesn't have this
                    "preferred_language_complexity": getattr(user_profile, 'preferred_language_complexity', 'medium'),
                    "preferred_response_style": getattr(user_profile, 'preferred_response_style', 'conversational')
                }
                
                # Use real OpenAI integration
                response = await self.openai_integration.generate_response(
                    input_text, personalization_params
                )
                
                print(f"✅ Generated OpenAI response for user {user_id}")
                
            except Exception as e:
                print(f"❌ OpenAI response generation failed: {e}")
                # Return error instead of fallback response
                return "I'm sorry, I'm having trouble connecting to my AI service right now. Please try again later."
            
            # Record bot response
            self.metrics_collector.record_bot_response(session_id, response, user_id)
            
            return response
            
        except Exception as e:
            print(f"❌ Error in process_user_input: {e}")
            return "I'm sorry, I encountered an error processing your message. Please try again."

    async def process_feedback(self, feedback_data: Dict[str, Any]) -> None:
        """Process user feedback - handles exact UI data structure"""
        try:
            session_id = feedback_data["session_id"]
            user_id = feedback_data["user_id"]
            
            # Record ALL feedback data from the UI
            self.metrics_collector.record_feedback(feedback_data)
            
            # Update user profile with ALL the feedback data
            self.user_profiler.update_profile_from_feedback(feedback_data)
            
            print(f"✅ Processed feedback for user {user_id}")
            
        except Exception as e:
            print(f"❌ Error processing feedback: {e}")

    async def process_session(self, session_data: Dict[str, Any]) -> None:
        """Process session data - handles exact UI data structure"""
        try:
            session_id = session_data["session_id"]
            user_id = session_data["user_id"]
            
            # Record ALL session data from the UI
            self.metrics_collector.record_session(session_data)
            
            print(f"✅ Processed session {session_id} for user {user_id}")
            
        except Exception as e:
            print(f"❌ Error processing session: {e}")

    def _get_rl_state(self, prompt_data: Dict[str, Any]) -> np.ndarray:
        """Convert prompt data to RL state vector - using ALL available data"""
        # Enhanced state representation using ALL the data from UI
        state = np.array([
            len(prompt_data.get("input_text", "")),  # Message length
            prompt_data.get("input_end_time", 0) - prompt_data.get("input_start_time", 0),  # Typing duration
            1.0 if prompt_data.get("user_id") else 0.0,  # User identified
            prompt_data.get("input_sent_time", 0) / 1000.0,  # Time since epoch (normalized)
        ], dtype=np.float32)
        return state

    def _generate_rl_response(self, input_text: str, action: np.ndarray, user_profile: UserProfile) -> str:
        """Generate response based on RL action"""
        try:
            # Decode action to strategy
            strategy = self._decode_action_to_strategy(action)
            
            # Create strategic prompt
            strategic_prompt = self._create_strategic_prompt(input_text, strategy, user_profile)
            
            # Extract personalization parameters from user profile
            personalization_params = {
                "temperature": 0.7,  # Default value since UserProfile doesn't have this
                "max_tokens": 1000,  # Default value since UserProfile doesn't have this
                "detail_level": getattr(user_profile, 'preferred_detail_level', 'medium'),
                "expertise_level": "beginner",  # Default value since UserProfile doesn't have this
                "preferred_language_complexity": getattr(user_profile, 'preferred_language_complexity', 'medium'),
                "preferred_response_style": getattr(user_profile, 'preferred_response_style', 'conversational')
            }
            
            # Generate response using OpenAI
            response = self.openai_integration.generate_response_sync(
                strategic_prompt, personalization_params
            )
            
            return response
            
        except Exception as e:
            print(f"⚠️  RL response generation failed: {e}")
            return f"I understand you said: '{input_text}'. How can I help you?"

    def _decode_action_to_strategy(self, action: np.ndarray) -> str:
        """Decode RL action to response strategy"""
        # Simple strategy mapping - you can enhance this
        if len(action) > 0:
            action_value = action[0]
            if action_value > 0.5:
                return "detailed"
            elif action_value > 0:
                return "balanced"
            else:
                return "concise"
        return "balanced"

    def _create_strategic_prompt(self, input_text: str, strategy: str, user_profile: UserProfile) -> str:
        """Create prompt based on RL strategy"""
        # Create a simple, natural prompt without verbose instructions
        if strategy == "detailed":
            return f"User asks: {input_text}\n\nProvide a helpful, detailed response with examples."
        elif strategy == "concise":
            return f"User asks: {input_text}\n\nProvide a brief, helpful response."
        else:
            return f"User asks: {input_text}\n\nProvide a helpful response with moderate detail."

    def _calculate_rl_reward(self, prompt_data: Dict[str, Any]) -> float:
        """Calculate reward for RL training - using ALL available data"""
        # Enhanced reward calculation using ALL the data from UI
        reward = 0.0
        
        # Reward for user engagement (typing duration)
        typing_duration = prompt_data.get("input_end_time", 0) - prompt_data.get("input_start_time", 0)
        if typing_duration > 1000:  # More than 1 second
            reward += 0.3
        
        # Reward for message length (user effort)
        message_length = len(prompt_data.get("input_text", ""))
        if message_length > 10:
            reward += 0.2
        
        # Reward for timely response (input_sent_time)
        current_time = int(datetime.now().timestamp() * 1000)
        sent_time = prompt_data.get("input_sent_time", current_time)
        time_diff = abs(current_time - sent_time)
        if time_diff < 5000:  # Within 5 seconds
            reward += 0.1
        
        # Normalize to [-1, 1]
        return max(-1.0, min(1.0, reward))

    async def _generate_fallback_response(self, input_text: str, user_profile: UserProfile) -> str:
        """Generate fallback response when RL fails"""
        try:
            # Extract personalization parameters from user profile
            personalization_params = {
                "temperature": 0.7,  # Default value since UserProfile doesn't have this
                "max_tokens": 1000,  # Default value since UserProfile doesn't have this
                "detail_level": getattr(user_profile, 'preferred_detail_level', 'medium'),
                "expertise_level": "beginner",  # Default value since UserProfile doesn't have this
                "preferred_language_complexity": getattr(user_profile, 'preferred_language_complexity', 'medium'),
                "preferred_response_style": getattr(user_profile, 'preferred_response_style', 'conversational')
            }
            
            return await self.openai_integration.generate_response(input_text, personalization_params)
        except Exception as e:
            print(f"⚠️  Fallback response generation failed: {e}")
            # Provide a more natural fallback response
            return f"Hi! I understand you said '{input_text}'. I'm here to help - what would you like to know more about?"

    def get_conversation_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get conversation status"""
        return self.active_conversations.get(session_id)

    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get user profile"""
        return self.user_profiler.get_user_profile(user_id) 