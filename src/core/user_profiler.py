"""
AI-Driven User Profiler for HumAIne-chatbot

This module implements the AI-driven user profiling system that creates comprehensive
user profiles using collected metrics, historical data, and reference data.
Implements the two-phase approach: Virtual Persona Pre-training and Online RL Adaptation.
"""

import time
from typing import Dict, Any, Optional
from datetime import datetime

from ..models.schemas import UserProfile
from .profile_persistence import ProfilePersistence
from .cross_session_learner import CrossSessionLearner
from ..utils.enhanced_language_analyzer import EnhancedLanguageAnalyzer

class UserProfiler:
    def __init__(self):
        self.user_profiles: Dict[str, UserProfile] = {}
        self.profile_update_history: Dict[str, list] = {}
        
        # Enhanced features
        self.profile_persistence = ProfilePersistence()
        self.cross_session_learner = CrossSessionLearner()
        self.language_analyzer = EnhancedLanguageAnalyzer()
        
        # Load existing profiles
        self._load_existing_profiles()
    
    def _load_existing_profiles(self):
        """Load existing profiles from disk"""
        try:
            existing_profiles = self.profile_persistence.load_all_profiles()
            self.user_profiles.update(existing_profiles)
            print(f"✅ Loaded {len(existing_profiles)} existing user profiles")
        except Exception as e:
            print(f"⚠️  Failed to load existing profiles: {e}")
    
    def create_user_profile(self, user_id: str) -> UserProfile:
        """Create a new user profile"""
        profile = UserProfile(
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            preferred_language_complexity="medium",
            preferred_detail_level="medium",
            preferred_response_style="conversational",
            average_session_duration=0.0,
            average_response_time=0.0,
            average_typing_speed=0.0,
            average_sentiment_score=0.0,
            average_language_complexity=0.0,
            average_grammatical_accuracy=1.0,
            total_sessions=0,
            average_engagement_time=0.0,
            feedback_ratio=0.0,
            positive_feedback_ratio=0.0,
            session_history=[],
            feedback_history=[],
            cross_session_insights={},
            rl_state={}
        )
        
        self.user_profiles[user_id] = profile
        self.profile_update_history[user_id] = []
        
        # Save to disk
        self.profile_persistence.save_profile(user_id, profile)
        
        return profile

    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get user profile by ID"""
        return self.user_profiles.get(user_id)

    def update_profile_from_prompt(self, prompt_data: Dict[str, Any]) -> None:
        """Update user profile based on prompt data - preserving ALL original data"""
        user_id = prompt_data["user_id"]
        profile = self.get_user_profile(user_id)
        
        if not profile:
            profile = self.create_user_profile(user_id)
        
        # Enhanced language analysis
        input_text = prompt_data.get("input_text", "")
        if input_text:
            language_analysis = self.language_analyzer.analyze_text(input_text)
            self._update_profile_from_language_analysis(profile, language_analysis)
        
        # Update profile metrics using ALL the data from UI
        self._update_profile_metrics(profile, prompt_data)
        
        # Update timestamp
        profile.updated_at = datetime.utcnow()
        
        # Store updated profile
        self.user_profiles[user_id] = profile
        
        # Save to disk
        self.profile_persistence.save_profile(user_id, profile)
        
        # Record update with ALL the original data
        self._record_profile_update(user_id, "prompt_update", prompt_data)
        
        # Update cross-session learning
        self._update_cross_session_learning(user_id)

    def update_profile_from_feedback(self, feedback_data: Dict[str, Any]) -> None:
        """Update user profile based on feedback data - preserving ALL original data"""
        user_id = feedback_data["user_id"]
        profile = self.get_user_profile(user_id)
        
        if not profile:
            profile = self.create_user_profile(user_id)
        
        # Update feedback counts using ALL the data from UI
        feedback_type = feedback_data.get("feedback_type", "neutral")
        
        if feedback_type == "positive":
            profile.feedback_history.append({
                "type": "positive",
                "timestamp": datetime.utcnow(),
                "response_text": feedback_data.get("response_text", ""),
                "response_duration": feedback_data.get("response_duration", 0),
                "feedback_delay_duration": feedback_data.get("feedback_delay_duration", 0)
            })
        elif feedback_type == "negative":
            profile.feedback_history.append({
                "type": "negative",
                "timestamp": datetime.utcnow(),
                "response_text": feedback_data.get("response_text", ""),
                "response_duration": feedback_data.get("response_duration", 0),
                "feedback_delay_duration": feedback_data.get("feedback_delay_duration", 0)
            })
        
        # Update personalization parameters based on feedback using ALL the data
        self._update_personalization_from_feedback(profile, feedback_data)
        
        # Update timestamp
        profile.updated_at = datetime.utcnow()
        
        # Store updated profile
        self.user_profiles[user_id] = profile
        
        # Save to disk
        self.profile_persistence.save_profile(user_id, profile)
        
        # Record update with ALL the original data
        self._record_profile_update(user_id, "feedback_update", feedback_data)
        
        # Update cross-session learning
        self._update_cross_session_learning(user_id)

    def _update_profile_from_language_analysis(self, profile: UserProfile, analysis: Dict[str, Any]) -> None:
        """Update profile based on enhanced language analysis"""
        try:
            # Update language complexity preference
            complexity_level = analysis.get('complexity_analysis', {}).get('complexity_level', 'medium')
            if complexity_level in ['very_easy', 'easy']:
                profile.preferred_language_complexity = 'simple'
            elif complexity_level in ['difficult', 'very_difficult']:
                profile.preferred_language_complexity = 'complex'
            else:
                profile.preferred_language_complexity = 'medium'
            
            # Update detail level based on vocabulary richness
            vocab_level = analysis.get('vocabulary_analysis', {}).get('vocabulary_level', 'medium')
            if vocab_level == 'advanced':
                profile.preferred_detail_level = 'detailed'
            elif vocab_level == 'limited':
                profile.preferred_detail_level = 'concise'
            
            # Update response style based on sentiment and enthusiasm
            sentiment_label = analysis.get('sentiment_analysis', {}).get('sentiment_label', 'neutral')
            enthusiasm_level = analysis.get('sentiment_analysis', {}).get('enthusiasm_level', 'low')
            
            if sentiment_label == 'positive' and enthusiasm_level == 'high':
                profile.preferred_response_style = 'enthusiastic'
            elif sentiment_label == 'negative':
                profile.preferred_response_style = 'professional'
            else:
                profile.preferred_response_style = 'conversational'
            
            # Note: expertise_level and personalization_parameters don't exist in UserProfile schema
            # These are handled by the dialogue manager with default values
            
        except Exception as e:
            print(f"⚠️  Failed to update profile from language analysis: {e}")

    def _update_profile_metrics(self, profile: UserProfile, prompt_data: Dict[str, Any]) -> None:
        """Update profile metrics from prompt data - using ALL available data"""
        # Update typing speed preference using exact timing data from UI
        typing_duration = prompt_data.get("input_end_time", 0) - prompt_data.get("input_start_time", 0)
        if typing_duration > 0:
            # Update average typing speed
            current_avg = profile.average_typing_speed
            message_length = len(prompt_data.get("input_text", ""))
            if message_length > 0:
                typing_speed = message_length / (typing_duration / 1000.0)  # chars per second
                profile.average_typing_speed = (current_avg + typing_speed) / 2
        
        # Update message length preference using exact text data from UI
        message_length = len(prompt_data.get("input_text", ""))
        if message_length > 100:
            profile.preferred_detail_level = "detailed"
        elif message_length < 20:
            profile.preferred_detail_level = "concise"
        
        # Update average response time
        input_sent_time = prompt_data.get("input_sent_time", 0)
        if input_sent_time > 0:
            # This could indicate user engagement patterns
            # Update average response time if we have previous data
            if profile.average_response_time > 0:
                profile.average_response_time = (profile.average_response_time + input_sent_time) / 2
            else:
                profile.average_response_time = input_sent_time

    def _update_personalization_from_feedback(self, profile: UserProfile, feedback_data: Dict[str, Any]) -> None:
        """Update personalization parameters based on feedback - using ALL available data"""
        feedback_type = feedback_data.get("feedback_type", "neutral")
        
        # Add feedback to history
        feedback_entry = {
            "type": feedback_type,
            "timestamp": datetime.utcnow(),
            "response_text": feedback_data.get("response_text", ""),
            "response_duration": feedback_data.get("response_duration", 0),
            "feedback_delay_duration": feedback_data.get("feedback_delay_duration", 0),
            "data": feedback_data  # Store complete original data
        }
        profile.feedback_history.append(feedback_entry)
        
        if feedback_type == "positive":
            # Increase detail level if positive feedback
            current_detail = profile.preferred_detail_level
            if current_detail == "concise":
                profile.preferred_detail_level = "medium"
            elif current_detail == "medium":
                profile.preferred_detail_level = "detailed"
            
            # Increase positive feedback ratio
            profile.positive_feedback_ratio = min(1.0, profile.positive_feedback_ratio + 0.1)
            
        elif feedback_type == "negative":
            # Decrease detail level if negative feedback
            current_detail = profile.preferred_detail_level
            if current_detail == "detailed":
                profile.preferred_detail_level = "medium"
            elif current_detail == "medium":
                profile.preferred_detail_level = "concise"
            
            # Decrease positive feedback ratio
            profile.positive_feedback_ratio = max(0.0, profile.positive_feedback_ratio - 0.1)
        
        # Update feedback ratio
        profile.feedback_ratio = min(1.0, profile.feedback_ratio + 0.1)
        
        # Update timestamp
        profile.updated_at = datetime.utcnow()
        
        print(f"✅ Updated profile for user {profile.user_id} based on {feedback_type} feedback")

    def _update_cross_session_learning(self, user_id: str) -> None:
        """Update cross-session learning for a user"""
        try:
            # Analyze patterns across all sessions
            patterns = self.cross_session_learner.analyze_user_patterns(user_id, self.user_profiles)
            
            # Apply insights to profile if available
            if patterns and 'insights' in patterns:
                profile = self.user_profiles.get(user_id)
                if profile:
                    # Store insights in profile for future use
                    if not hasattr(profile, 'cross_session_insights'):
                        profile.cross_session_insights = {}
                    
                    profile.cross_session_insights.update(patterns)
                    
        except Exception as e:
            print(f"⚠️  Failed to update cross-session learning: {e}")

    def _record_profile_update(self, user_id: str, update_type: str, data: Dict[str, Any]) -> None:
        """Record profile update for audit trail - preserving ALL original data"""
        if user_id not in self.profile_update_history:
            self.profile_update_history[user_id] = []
        
        self.profile_update_history[user_id].append({
            "timestamp": datetime.utcnow(),
            "type": update_type,
            "data": data  # Store the complete original data
        })

    def get_personalization_parameters(self, user_id: str) -> Dict[str, Any]:
        """Get personalization parameters for a user"""
        profile = self.get_user_profile(user_id)
        if profile:
            return profile.personalization_parameters
        return {}

    def update_profile_from_session(self, user_id: str, session_data: Dict[str, Any]) -> Optional[UserProfile]:
        """Update user profile based on session data - preserving ALL original data"""
        profile = self.get_user_profile(user_id)
        if not profile:
            return None
        
        # Add session to history using ALL the data from UI
        session_entry = {
            "session_id": session_data.get("session_id"),
            "start_time": session_data.get("session_start"),
            "end_time": session_data.get("session_end"),
            "duration": session_data.get("session_duration"),
            "end_type": session_data.get("session_end_type"),
            "data": session_data  # Store complete original data
        }
        profile.session_history.append(session_entry)
        
        # Update session metrics
        profile.total_sessions += 1
        
        # Update average session duration
        if session_data.get("session_duration"):
            current_avg = profile.average_session_duration
            new_duration = session_data["session_duration"]
            if current_avg > 0:
                profile.average_session_duration = (current_avg + new_duration) / 2
            else:
                profile.average_session_duration = new_duration
        
        # Update average engagement time if available
        if session_data.get("engagement", {}).get("engagement_time"):
            engagement_time = session_data["engagement"]["engagement_time"]
            current_avg = profile.average_engagement_time
            if current_avg > 0:
                profile.average_engagement_time = (current_avg + engagement_time) / 2
            else:
                profile.average_engagement_time = engagement_time
        
        # Update timestamp
        profile.updated_at = datetime.utcnow()
        
        # Store updated profile
        self.user_profiles[user_id] = profile
        
        # Save to disk
        self.profile_persistence.save_profile(user_id, profile)
        
        # Update cross-session learning
        self._update_cross_session_learning(user_id)
        
        print(f"✅ Updated profile for user {user_id} with session data")
        
        return profile

    def get_all_profiles(self) -> Dict[str, UserProfile]:
        """Get all user profiles"""
        return self.user_profiles.copy()

    def delete_user_profile(self, user_id: str) -> bool:
        """Delete a user profile"""
        if user_id in self.user_profiles:
            del self.user_profiles[user_id]
            if user_id in self.profile_update_history:
                del self.profile_update_history[user_id]
            
            # Delete from disk
            self.profile_persistence.delete_profile(user_id)
            
            # Clear cross-session cache
            self.cross_session_learner.clear_cache(user_id)
            
            return True
        return False
    
    def get_user_insights(self, user_id: str) -> Dict[str, Any]:
        """Get cross-session insights for a user"""
        return self.cross_session_learner.get_user_insights(user_id)
    
    def get_profile_stats(self) -> Dict[str, Any]:
        """Get statistics about all profiles"""
        return self.profile_persistence.get_profile_stats()
    
    def save_all_profiles(self) -> bool:
        """Save all profiles to disk"""
        try:
            for user_id, profile in self.user_profiles.items():
                self.profile_persistence.save_profile(user_id, profile)
            return True
        except Exception as e:
            print(f"❌ Failed to save all profiles: {e}")
            return False 