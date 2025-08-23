"""
Reinforcement Learning Agent for HumAIne-chatbot

This module implements the RL environment and agent for the chatbot system,
enabling online adaptation based on user engagement and feedback.
"""

import gymnasium as gym
import numpy as np
from typing import Dict, Any, Tuple, Optional
from gymnasium import spaces

from ..models.schemas import UserProfile


class ChatbotEnvironment(gym.Env):
    """Gym environment for chatbot reinforcement learning"""
    
    def __init__(self, user_profile: UserProfile):
        """
        Initialize the chatbot environment
        
        Args:
            user_profile: User profile for personalization
        """
        super().__init__()
        
        self.user_profile = user_profile
        self.current_state = None
        self.step_count = 0
        self.max_steps = 50  # Maximum conversation turns
        
        # Define action space (response strategies)
        # Actions: [language_complexity, response_style, detail_level, sentiment_tone]
        self.action_space = spaces.Box(
            low=np.array([0, 0, 0, 0]),
            high=np.array([1, 1, 1, 1]),
            dtype=np.float32
        )
        
        # Define observation space (user state)
        # State: [session_duration, response_time, typing_speed, sentiment, 
        #         language_complexity, grammar_accuracy, engagement_ratio, feedback_ratio]
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, -1, 0, 0, 0, 0]),
            high=np.array([1, 1, 1, 1, 1, 1, 1, 1]),
            dtype=np.float32
        )
        
        # Initialize state
        self.reset()
    
    def reset(self, seed: Optional[int] = None) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Reset the environment"""
        super().reset(seed=seed)
        
        self.step_count = 0
        
        # Initialize state based on user profile
        self.current_state = self._get_initial_state()
        
        return self.current_state, {}
    
    def step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        """
        Take a step in the environment
        
        Args:
            action: Action vector [language_complexity, response_style, detail_level, sentiment_tone]
            
        Returns:
            Tuple of (observation, reward, terminated, truncated, info)
        """
        self.step_count += 1
        
        # Apply action to generate response strategy
        response_strategy = self._apply_action(action)
        
        # Simulate user response (in practice, this would be real user interaction)
        user_response = self._simulate_user_response(response_strategy)
        
        # Calculate reward based on user response
        reward = self._calculate_reward(user_response, response_strategy)
        
        # Update state
        self.current_state = self._update_state(user_response)
        
        # Check if episode is done
        done = self.step_count >= self.max_steps or self._should_end_conversation()
        
        info = {
            'response_strategy': response_strategy,
            'user_response': user_response,
            'step_count': self.step_count
        }
        
        return self.current_state, reward, done, False, info
    
    def _get_initial_state(self) -> np.ndarray:
        """Get initial state based on user profile"""
        return np.array([
            min(self.user_profile.average_session_duration / 60000, 1.0),  # Normalize to [0, 1]
            min(self.user_profile.average_response_time / 10000, 1.0),
            min(self.user_profile.average_typing_speed / 10, 1.0),
            self.user_profile.average_sentiment_score / 5.0,  # Normalize to [-1, 1]
            self.user_profile.average_language_complexity,
            self.user_profile.average_grammatical_accuracy,
            min(self.user_profile.average_engagement_time / self.user_profile.average_session_duration, 1.0) if self.user_profile.average_session_duration > 0 else 0.5,
            self.user_profile.feedback_ratio
        ], dtype=np.float32)
    
    def _apply_action(self, action: np.ndarray) -> Dict[str, Any]:
        """Apply action to generate response strategy"""
        language_complexity, response_style, detail_level, sentiment_tone = action
        
        # Map continuous values to discrete strategies
        complexity_levels = ["simple", "medium", "complex"]
        style_levels = ["conversational", "balanced", "professional"]
        detail_levels = ["concise", "medium", "detailed"]
        sentiment_levels = ["neutral", "positive", "enthusiastic"]
        
        return {
            "language_complexity": complexity_levels[int(language_complexity * 2.99)],
            "response_style": style_levels[int(response_style * 2.99)],
            "detail_level": detail_levels[int(detail_level * 2.99)],
            "sentiment_tone": sentiment_levels[int(sentiment_tone * 2.99)]
        }
    
    def _simulate_user_response(self, response_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate user response based on strategy and user profile"""
        # This is a simplified simulation - in practice, this would be real user interaction
        
        # Calculate compatibility score between strategy and user preferences
        compatibility_score = self._calculate_compatibility(response_strategy)
        
        # Simulate user engagement
        engagement_prob = min(compatibility_score * 0.8 + 0.2, 1.0)
        is_engaged = np.random.random() < engagement_prob
        
        # Simulate feedback
        feedback_prob = compatibility_score * 0.6 + 0.2
        gives_feedback = np.random.random() < feedback_prob
        
        if gives_feedback:
            feedback_type = "positive" if compatibility_score > 0.6 else "negative"
        else:
            feedback_type = "none"
        
        # Simulate sentiment
        base_sentiment = self.user_profile.average_sentiment_score / 5.0
        sentiment_change = (compatibility_score - 0.5) * 0.3
        simulated_sentiment = np.clip(base_sentiment + sentiment_change, -1, 1)
        
        return {
            "engagement": is_engaged,
            "feedback_type": feedback_type,
            "sentiment": simulated_sentiment,
            "response_time": self._simulate_response_time(compatibility_score),
            "message_length": self._simulate_message_length(compatibility_score)
        }
    
    def _calculate_compatibility(self, strategy: Dict[str, Any]) -> float:
        """Calculate compatibility between strategy and user preferences"""
        compatibility = 0.0
        
        # Language complexity compatibility
        complexity_map = {"simple": 0.3, "medium": 0.6, "complex": 0.9}
        user_complexity = complexity_map.get(self.user_profile.preferred_language_complexity, 0.5)
        strategy_complexity = complexity_map.get(strategy["language_complexity"], 0.5)
        complexity_compat = 1.0 - abs(user_complexity - strategy_complexity)
        
        # Response style compatibility
        style_map = {"conversational": 0.3, "balanced": 0.5, "professional": 0.7}
        user_style = style_map.get(self.user_profile.preferred_response_style, 0.5)
        strategy_style = style_map.get(strategy["response_style"], 0.5)
        style_compat = 1.0 - abs(user_style - strategy_style)
        
        # Detail level compatibility
        detail_map = {"concise": 0.3, "medium": 0.5, "detailed": 0.7}
        user_detail = detail_map.get(self.user_profile.preferred_detail_level, 0.5)
        strategy_detail = detail_map.get(strategy["detail_level"], 0.5)
        detail_compat = 1.0 - abs(user_detail - strategy_detail)
        
        # Sentiment compatibility
        sentiment_compat = 1.0 - abs(self.user_profile.average_sentiment_score / 5.0)
        
        # Weighted average
        compatibility = (
            complexity_compat * 0.3 +
            style_compat * 0.3 +
            detail_compat * 0.2 +
            sentiment_compat * 0.2
        )
        
        return compatibility
    
    def _simulate_response_time(self, compatibility: float) -> float:
        """Simulate user response time based on compatibility"""
        base_time = self.user_profile.average_response_time / 1000  # Convert to seconds
        # Lower compatibility = longer response time
        time_multiplier = 1.0 + (1.0 - compatibility) * 0.5
        return base_time * time_multiplier
    
    def _simulate_message_length(self, compatibility: float) -> int:
        """Simulate message length based on compatibility"""
        base_length = 20  # Average message length
        # Higher compatibility = longer messages
        length_multiplier = 0.5 + compatibility * 1.0
        return int(base_length * length_multiplier)
    
    def _calculate_reward(self, user_response: Dict[str, Any], 
                         strategy: Dict[str, Any]) -> float:
        """Calculate reward based on user response and strategy"""
        reward = 0.0
        
        # Engagement reward
        if user_response["engagement"]:
            reward += 0.4
        
        # Feedback reward
        if user_response["feedback_type"] == "positive":
            reward += 0.3
        elif user_response["feedback_type"] == "negative":
            reward -= 0.2
        
        # Sentiment reward
        sentiment_reward = (user_response["sentiment"] + 1) / 2  # Normalize to [0, 1]
        reward += sentiment_reward * 0.2
        
        # Response time reward (faster = better)
        response_time_reward = max(0, 1 - user_response["response_time"] / 10)
        reward += response_time_reward * 0.1
        
        # Message length reward (longer = more engaged)
        length_reward = min(user_response["message_length"] / 50, 1.0)
        reward += length_reward * 0.1
        
        return reward
    
    def _update_state(self, user_response: Dict[str, Any]) -> np.ndarray:
        """Update state based on user response"""
        # Simplified state update - in practice, this would be more sophisticated
        current_state = self.current_state.copy()
        
        # Update engagement ratio
        if user_response["engagement"]:
            current_state[6] = min(current_state[6] + 0.1, 1.0)
        else:
            current_state[6] = max(current_state[6] - 0.05, 0.0)
        
        # Update sentiment
        current_state[3] = np.clip(current_state[3] + user_response["sentiment"] * 0.1, -1, 1)
        
        # Update feedback ratio
        if user_response["feedback_type"] != "none":
            current_state[7] = min(current_state[7] + 0.1, 1.0)
        
        return current_state
    
    def _should_end_conversation(self) -> bool:
        """Determine if conversation should end"""
        # End if low engagement or negative sentiment
        if self.current_state[6] < 0.2 or self.current_state[3] < -0.5:
            return True
        
        # End if high engagement and positive feedback (successful conversation)
        if self.current_state[6] > 0.8 and self.current_state[7] > 0.7:
            return True
        
        return False
    
    def render(self):
        """Render the environment (for debugging)"""
        print(f"Step: {self.step_count}")
        print(f"State: {self.current_state}")
        print(f"User Profile: {self.user_profile.user_id}")
        print(f"Engagement: {self.current_state[6]:.2f}")
        print(f"Sentiment: {self.current_state[3]:.2f}")
        print(f"Feedback Ratio: {self.current_state[7]:.2f}")
        print("-" * 50)


class ChatbotRLAgent:
    """Reinforcement learning agent for chatbot personalization"""
    
    def __init__(self, user_profile: UserProfile):
        """
        Initialize the RL agent
        
        Args:
            user_profile: User profile for personalization
        """
        self.user_profile = user_profile
        self.environment = ChatbotEnvironment(user_profile)
        self.action_history = []
        self.reward_history = []
    
    def get_action(self, state: np.ndarray) -> np.ndarray:
        """Get action from current state"""
        # This would be replaced by the actual RL policy
        # For now, use a simple heuristic based on user profile
        
        # Map user preferences to action space
        complexity_map = {"simple": 0.2, "medium": 0.5, "complex": 0.8}
        style_map = {"conversational": 0.2, "balanced": 0.5, "professional": 0.8}
        detail_map = {"concise": 0.2, "medium": 0.5, "detailed": 0.8}
        
        action = np.array([
            complexity_map.get(self.user_profile.preferred_language_complexity, 0.5),
            style_map.get(self.user_profile.preferred_response_style, 0.5),
            detail_map.get(self.user_profile.preferred_detail_level, 0.5),
            0.5  # Neutral sentiment tone
        ], dtype=np.float32)
        
        # Add some exploration noise
        noise = np.random.normal(0, 0.1, 4)
        action = np.clip(action + noise, 0, 1)
        
        return action
    
    def update_policy(self, state: np.ndarray, action: np.ndarray, 
                     reward: float, next_state: np.ndarray):
        """Update the policy based on experience"""
        # Store experience for offline training
        self.action_history.append({
            'state': state,
            'action': action,
            'reward': reward,
            'next_state': next_state
        })
        
        self.reward_history.append(reward)
        
        # Keep only recent history
        if len(self.action_history) > 100:
            self.action_history = self.action_history[-100:]
            self.reward_history = self.reward_history[-100:]
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """Get performance metrics"""
        if not self.reward_history:
            return {}
        
        return {
            'average_reward': np.mean(self.reward_history),
            'total_reward': np.sum(self.reward_history),
            'reward_std': np.std(self.reward_history),
            'episode_count': len(self.reward_history)
        } 