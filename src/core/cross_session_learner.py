"""
Cross-Session Learning for HumAIne-chatbot

This module analyzes user behavior patterns across multiple sessions
to provide deeper insights and better personalization.
"""

import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, Counter

from ..models.schemas import UserProfile

class CrossSessionLearner:
    """Analyzes user behavior patterns across multiple sessions"""
    
    def __init__(self):
        self.pattern_cache = {}
        self.learning_weights = {
            'recent': 0.5,      # Recent sessions have higher weight
            'frequency': 0.3,   # Frequently occurring patterns
            'consistency': 0.2   # Consistent behavior patterns
        }
    
    def analyze_user_patterns(self, user_id: str, profiles: Dict[str, UserProfile]) -> Dict[str, Any]:
        """Analyze patterns across all sessions for a user"""
        if user_id not in profiles:
            return {}
        
        profile = profiles[user_id]
        if not profile.session_history:
            return {}
        
        # Analyze different aspects
        timing_patterns = self._analyze_timing_patterns(profile)
        engagement_patterns = self._analyze_engagement_patterns(profile)
        communication_patterns = self._analyze_communication_patterns(profile)
        feedback_patterns = self._analyze_feedback_patterns(profile)
        
        # Generate insights
        insights = self._generate_insights(
            timing_patterns, 
            engagement_patterns, 
            communication_patterns, 
            feedback_patterns
        )
        
        # Update pattern cache
        self.pattern_cache[user_id] = {
            'timing': timing_patterns,
            'engagement': engagement_patterns,
            'communication': communication_patterns,
            'feedback': feedback_patterns,
            'insights': insights,
            'last_updated': datetime.utcnow()
        }
        
        return {
            'patterns': {
                'timing': timing_patterns,
                'engagement': engagement_patterns,
                'communication': communication_patterns,
                'feedback': feedback_patterns
            },
            'insights': insights,
            'recommendations': self._generate_recommendations(insights)
        }
    
    def _analyze_timing_patterns(self, profile: UserProfile) -> Dict[str, Any]:
        """Analyze timing-related patterns"""
        sessions = profile.session_history
        if not sessions:
            return {}
        
        # Session duration patterns
        durations = [s.get('duration', 0) for s in sessions if s.get('duration')]
        avg_duration = np.mean(durations) if durations else 0
        
        # Time of day patterns
        time_patterns = defaultdict(int)
        for session in sessions:
            if session.get('start_time'):
                try:
                    start_time = datetime.fromtimestamp(session['start_time'] / 1000)
                    hour = start_time.hour
                    if 6 <= hour < 12:
                        time_patterns['morning'] += 1
                    elif 12 <= hour < 17:
                        time_patterns['afternoon'] += 1
                    elif 17 <= hour < 22:
                        time_patterns['evening'] += 1
                    else:
                        time_patterns['night'] += 1
                except:
                    pass
        
        # Frequency patterns
        session_frequency = len(sessions) / max(1, (datetime.utcnow() - profile.created_at).days)
        
        return {
            'avg_session_duration': avg_duration,
            'total_sessions': len(sessions),
            'session_frequency_per_day': session_frequency,
            'time_preferences': dict(time_patterns),
            'duration_consistency': np.std(durations) if len(durations) > 1 else 0
        }
    
    def _analyze_engagement_patterns(self, profile: UserProfile) -> Dict[str, Any]:
        """Analyze user engagement patterns"""
        sessions = profile.session_history
        if not sessions:
            return {}
        
        # Engagement level based on session duration and frequency
        recent_sessions = [s for s in sessions if s.get('start_time')]
        if recent_sessions:
            recent_sessions.sort(key=lambda x: x.get('start_time', 0), reverse=True)
            recent_avg_duration = np.mean([s.get('duration', 0) for s in recent_sessions[:5]])
        else:
            recent_avg_duration = 0
        
        # Engagement trend
        if len(sessions) > 1:
            early_sessions = sessions[:len(sessions)//2]
            late_sessions = sessions[len(sessions)//2:]
            
            early_avg_duration = np.mean([s.get('duration', 0) for s in early_sessions])
            late_avg_duration = np.mean([s.get('duration', 0) for s in late_sessions])
            
            engagement_trend = 'increasing' if late_avg_duration > early_avg_duration else 'decreasing'
        else:
            engagement_trend = 'stable'
        
        return {
            'recent_engagement': recent_avg_duration,
            'engagement_trend': engagement_trend,
            'engagement_level': self._classify_engagement_level(recent_avg_duration),
            'session_completion_rate': self._calculate_completion_rate(sessions)
        }
    
    def _analyze_communication_patterns(self, profile: UserProfile) -> Dict[str, Any]:
        """Analyze communication style patterns"""
        # Language complexity preferences
        complexity_prefs = profile.preferred_language_complexity
        detail_prefs = profile.preferred_detail_level
        style_prefs = profile.preferred_response_style
        
        # Communication consistency
        consistency_score = 0
        if complexity_prefs == 'intermediate':
            consistency_score += 0.3
        if detail_prefs == 'balanced':
            consistency_score += 0.3
        if style_prefs == 'conversational':
            consistency_score += 0.4
        
        # Expertise progression
        expertise_progression = self._analyze_expertise_progression(profile)
        
        return {
            'preferred_complexity': complexity_prefs,
            'preferred_detail': detail_prefs,
            'preferred_style': style_prefs,
            'communication_consistency': consistency_score,
            'expertise_progression': expertise_progression,
            'adaptability_score': self._calculate_adaptability_score(profile)
        }
    
    def _analyze_feedback_patterns(self, profile: UserProfile) -> Dict[str, Any]:
        """Analyze user feedback patterns"""
        feedback_history = profile.feedback_history
        if not feedback_history:
            return {}
        
        # Feedback type distribution
        feedback_types = [f.get('type', 'neutral') for f in feedback_history]
        feedback_counter = Counter(feedback_types)
        
        # Feedback timing patterns
        feedback_delays = [f.get('feedback_delay_duration', 0) for f in feedback_history if f.get('feedback_delay_duration')]
        avg_feedback_delay = np.mean(feedback_delays) if feedback_delays else 0
        
        # Feedback consistency
        positive_ratio = feedback_counter.get('positive', 0) / len(feedback_history)
        negative_ratio = feedback_counter.get('negative', 0) / len(feedback_history)
        
        # Feedback improvement pattern
        improvement_pattern = self._analyze_feedback_improvement(feedback_history)
        
        return {
            'total_feedback': len(feedback_history),
            'positive_ratio': positive_ratio,
            'negative_ratio': negative_ratio,
            'avg_feedback_delay': avg_feedback_delay,
            'feedback_consistency': 1 - abs(positive_ratio - negative_ratio),
            'improvement_pattern': improvement_pattern,
            'feedback_engagement': self._classify_feedback_engagement(feedback_history)
        }
    
    def _analyze_expertise_progression(self, profile: UserProfile) -> Dict[str, Any]:
        """Analyze how user expertise has evolved"""
        sessions = profile.session_history
        if len(sessions) < 2:
            return {'progression': 'insufficient_data'}
        
        # Simple progression based on session count and duration
        early_sessions = sessions[:len(sessions)//2]
        late_sessions = sessions[len(sessions)//2:]
        
        early_avg_duration = np.mean([s.get('duration', 0) for s in early_sessions])
        late_avg_duration = np.mean([s.get('duration', 0) for s in late_sessions])
        
        if late_avg_duration > early_avg_duration * 1.2:
            progression = 'improving'
        elif late_avg_duration < early_avg_duration * 0.8:
            progression = 'declining'
        else:
            progression = 'stable'
        
        return {
            'progression': progression,
            'early_avg_duration': early_avg_duration,
            'late_avg_duration': late_avg_duration,
            'improvement_ratio': late_avg_duration / max(early_avg_duration, 1)
        }
    
    def _analyze_feedback_improvement(self, feedback_history: List[Dict]) -> str:
        """Analyze if feedback is improving over time"""
        if len(feedback_history) < 3:
            return 'insufficient_data'
        
        # Check if recent feedback is more positive
        recent_feedback = feedback_history[-3:]
        early_feedback = feedback_history[:3]
        
        recent_positive = sum(1 for f in recent_feedback if f.get('type') == 'positive')
        early_positive = sum(1 for f in early_feedback if f.get('type') == 'positive')
        
        if recent_positive > early_positive:
            return 'improving'
        elif recent_positive < early_positive:
            return 'declining'
        else:
            return 'stable'
    
    def _calculate_completion_rate(self, sessions: List[Dict]) -> float:
        """Calculate session completion rate"""
        if not sessions:
            return 0.0
        
        completed_sessions = sum(1 for s in sessions if s.get('session_end_type') == 'completed')
        return completed_sessions / len(sessions)
    
    def _calculate_adaptability_score(self, profile: UserProfile) -> float:
        """Calculate how well user adapts to different communication styles"""
        # This is a simplified version - in practice, you'd analyze actual interactions
        adaptability_score = 0.5  # Base score
        
        # Adjust based on feedback patterns
        if profile.feedback_history:
            positive_feedback = sum(1 for f in profile.feedback_history if f.get('type') == 'positive')
            total_feedback = len(profile.feedback_history)
            if total_feedback > 0:
                adaptability_score += (positive_feedback / total_feedback) * 0.3
        
        # Adjust based on session variety
        if len(profile.session_history) > 1:
            adaptability_score += min(0.2, len(profile.session_history) * 0.02)
        
        return min(1.0, adaptability_score)
    
    def _classify_engagement_level(self, avg_duration: float) -> str:
        """Classify user engagement level"""
        if avg_duration > 300000:  # 5 minutes
            return 'high'
        elif avg_duration > 120000:  # 2 minutes
            return 'medium'
        else:
            return 'low'
    
    def _classify_feedback_engagement(self, feedback_history: List[Dict]) -> str:
        """Classify user feedback engagement level"""
        if not feedback_history:
            return 'none'
        
        # Check feedback frequency and timing
        total_feedback = len(feedback_history)
        avg_delay = np.mean([f.get('feedback_delay_duration', 0) for f in feedback_history if f.get('feedback_delay_duration')])
        
        if total_feedback > 5 and avg_delay < 10000:  # Quick feedback
            return 'high'
        elif total_feedback > 2:
            return 'medium'
        else:
            return 'low'
    
    def _generate_insights(self, timing: Dict, engagement: Dict, communication: Dict, feedback: Dict) -> List[str]:
        """Generate human-readable insights from patterns"""
        insights = []
        
        # Timing insights
        if timing.get('session_frequency_per_day', 0) > 2:
            insights.append("User is highly active with multiple daily sessions")
        elif timing.get('session_frequency_per_day', 0) < 0.1:
            insights.append("User has infrequent usage patterns")
        
        # Engagement insights
        if engagement.get('engagement_trend') == 'increasing':
            insights.append("User engagement is improving over time")
        elif engagement.get('engagement_trend') == 'decreasing':
            insights.append("User engagement has declined recently")
        
        # Communication insights
        if communication.get('communication_consistency', 0) > 0.8:
            insights.append("User has consistent communication preferences")
        else:
            insights.append("User shows varied communication preferences")
        
        # Feedback insights
        if feedback.get('positive_ratio', 0) > 0.7:
            insights.append("User is generally satisfied with responses")
        elif feedback.get('negative_ratio', 0) > 0.5:
            insights.append("User frequently provides negative feedback")
        
        return insights
    
    def _generate_recommendations(self, insights: List[str]) -> List[str]:
        """Generate recommendations based on insights"""
        recommendations = []
        
        for insight in insights:
            if "highly active" in insight:
                recommendations.append("Consider providing more detailed responses to maintain engagement")
            elif "infrequent usage" in insight:
                recommendations.append("Focus on concise, impactful responses to encourage return visits")
            elif "engagement improving" in insight:
                recommendations.append("Continue current approach as it's working well")
            elif "engagement declined" in insight:
                recommendations.append("Review recent interactions and adjust response strategy")
            elif "consistent preferences" in insight:
                recommendations.append("Maintain current personalization approach")
            elif "varied preferences" in insight:
                recommendations.append("Adapt responses dynamically based on context")
            elif "generally satisfied" in insight:
                recommendations.append("Maintain current response quality and style")
            elif "negative feedback" in insight:
                recommendations.append("Review and improve response accuracy and relevance")
        
        return recommendations
    
    def get_user_insights(self, user_id: str) -> Dict[str, Any]:
        """Get cached insights for a user"""
        return self.pattern_cache.get(user_id, {})
    
    def clear_cache(self, user_id: Optional[str] = None):
        """Clear pattern cache"""
        if user_id:
            self.pattern_cache.pop(user_id, None)
        else:
            self.pattern_cache.clear()
