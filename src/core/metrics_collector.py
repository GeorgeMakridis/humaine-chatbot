"""
Personalization Metrics Collector for HumAIne-chatbot

This module is responsible for gathering and analyzing metrics during user interactions,
including both implicit and explicit metrics as described in the research paper.
"""

import time
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

class MetricsCollector:
    def __init__(self):
        self.session_metrics: Dict[str, List[Dict[str, Any]]] = {}
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.user_metrics: Dict[str, Dict[str, Any]] = {}

    def start_session(self, user_id: str) -> str:
        """Start a new session and return session ID"""
        session_id = f"session_{int(time.time() * 1000)}_{user_id}"
        
        self.active_sessions[session_id] = {
            'user_id': user_id,
            'start_time': int(time.time() * 1000),
            'last_activity': int(time.time() * 1000),
            'turn_count': 0
        }
        
        self.session_metrics[session_id] = []
        
        return session_id

    def record_user_prompt(self, prompt_data: Dict[str, Any]) -> None:
        """Record user prompt data - preserving ALL original data from UI"""
        session_id = prompt_data["session_id"]
        
        # Create session if it doesn't exist, but use the provided session_id
        if session_id not in self.session_metrics:
            # Initialize the session with the provided session_id instead of creating a new one
            self.session_metrics[session_id] = []
            self.active_sessions[session_id] = {
                'user_id': prompt_data["user_id"],
                'start_time': prompt_data.get("input_start_time", int(time.time() * 1000)),
                'last_activity': prompt_data.get("input_sent_time", int(time.time() * 1000)),
                'turn_count': 0
            }
        
        # Store ALL the original data from the UI
        self.session_metrics[session_id].append({
            'type': 'user_prompt',
            'timestamp': prompt_data.get("input_sent_time", int(time.time() * 1000)),
            'data': prompt_data,  # Store the complete original data
            'extracted_metrics': {
                'input_text': prompt_data.get("input_text", ""),
                'input_start_time': prompt_data.get("input_start_time", 0),
                'input_end_time': prompt_data.get("input_end_time", 0),
                'input_sent_time': prompt_data.get("input_sent_time", 0),
                'typing_duration': prompt_data.get("input_end_time", 0) - prompt_data.get("input_start_time", 0),
                'message_length': len(prompt_data.get("input_text", ""))
            }
        })
        
        if session_id in self.active_sessions:
            self.active_sessions[session_id]['last_activity'] = prompt_data.get("input_sent_time", int(time.time() * 1000))

    def record_bot_response(self, session_id: str, response: str, user_id: str) -> None:
        """Record bot response"""
        if session_id in self.session_metrics:
            self.session_metrics[session_id].append({
                'type': 'bot_response',
                'timestamp': int(time.time() * 1000),
                'response': response,
                'user_id': user_id
            })
            if session_id in self.active_sessions:
                self.active_sessions[session_id]['turn_count'] += 1
                self.active_sessions[session_id]['last_activity'] = int(time.time() * 1000)

    def record_feedback(self, feedback_data: Dict[str, Any]) -> None:
        """Record user feedback - preserving ALL original data from UI"""
        session_id = feedback_data["session_id"]
        
        # Create session if it doesn't exist, but use the provided session_id
        if session_id not in self.session_metrics:
            # Initialize the session with the provided session_id instead of creating a new one
            self.session_metrics[session_id] = []
            self.active_sessions[session_id] = {
                'user_id': feedback_data["user_id"],
                'start_time': feedback_data.get("response_start_time", int(time.time() * 1000)),
                'last_activity': feedback_data.get("feedback_time", int(time.time() * 1000)),
                'turn_count': 0
            }
        
        # Store ALL the original feedback data from the UI
        self.session_metrics[session_id].append({
            'type': 'feedback',
            'timestamp': feedback_data.get("feedback_time", int(time.time() * 1000)),
            'data': feedback_data,  # Store the complete original data
            'extracted_metrics': {
                'response_text': feedback_data.get("response_text", ""),
                'response_start_time': feedback_data.get("response_start_time", 0),
                'response_end_time': feedback_data.get("response_end_time", 0),
                'response_duration': feedback_data.get("response_duration", 0),
                'feedback_type': feedback_data.get("feedback_type", ""),
                'feedback_time': feedback_data.get("feedback_time", 0),
                'feedback_delay_duration': feedback_data.get("feedback_delay_duration", 0)
            }
        })

    def record_session(self, session_data: Dict[str, Any]) -> None:
        """Record session data - preserving ALL original data from UI"""
        session_id = session_data["session_id"]
        
        # Create session if it doesn't exist
        if session_id not in self.session_metrics:
            self.start_session(session_data["user_id"])
        
        # Store ALL the original session data from the UI
        self.session_metrics[session_id].append({
            'type': 'session',
            'timestamp': int(time.time() * 1000),
            'data': session_data,  # Store the complete original data
            'extracted_metrics': {
                'session_start': session_data.get("session_start", 0),
                'session_end': session_data.get("session_end", 0),
                'session_end_type': session_data.get("session_end_type", ""),
                'session_duration': session_data.get("session_duration", 0)
            }
        })

    def record_user_message(self, session_id: str, message: str, typing_start_time: int, 
                           typing_end_time: int, sent_time: int, bot_message_time: Optional[int] = None) -> Dict[str, Any]:
        """Record a user message with timing information"""
        if session_id not in self.session_metrics:
            self.start_session(session_id)
        
        user_prompt = {
            'type': 'user_message',
            'timestamp': sent_time,
            'message': message,
            'typing_start_time': typing_start_time,
            'typing_end_time': typing_end_time,
            'typing_duration': typing_end_time - typing_start_time,
            'bot_message_time': bot_message_time
        }
        
        self.session_metrics[session_id].append(user_prompt)
        
        if session_id in self.active_sessions:
            self.active_sessions[session_id]['last_activity'] = sent_time
            self.active_sessions[session_id]['turn_count'] += 1
        
        return user_prompt

    def record_feedback(self, session_id: str, response_text: str, response_start_time: int,
                       response_end_time: int, feedback_type: str, feedback_time: int) -> Dict[str, Any]:
        """Record user feedback on a bot response"""
        if session_id not in self.session_metrics:
            return {}
        
        feedback = {
            'type': 'feedback',
            'timestamp': feedback_time,
            'response_text': response_text,
            'response_start_time': response_start_time,
            'response_end_time': response_end_time,
            'response_duration': response_end_time - response_start_time,
            'feedback_type': feedback_type
        }
        
        self.session_metrics[session_id].append(feedback)
        return feedback

    def end_session(self, session_id: str, end_type: str = "userAction") -> Optional[Dict[str, Any]]:
        """End a session and return session data"""
        if session_id not in self.active_sessions:
            return None
        
        session_data = {
            'session_id': session_id,
            'user_id': self.active_sessions[session_id]['user_id'],
            'start_time': self.active_sessions[session_id]['start_time'],
            'end_time': int(time.time() * 1000),
            'end_type': end_type,
            'turn_count': self.active_sessions[session_id]['turn_count'],
            'total_duration': int(time.time() * 1000) - self.active_sessions[session_id]['start_time']
        }
        
        # Remove from active sessions
        del self.active_sessions[session_id]
        
        return session_data

    def get_session_metrics(self, session_id: str) -> List[Dict[str, Any]]:
        """Get metrics for a specific session"""
        return self.session_metrics.get(session_id, [])

    def get_user_metrics(self, user_id: str) -> Dict[str, Any]:
        """Get metrics for a specific user"""
        return self.user_metrics.get(user_id, {})

    def get_user_metrics_count(self, user_id: str) -> int:
        """Get the number of metrics collected for a user"""
        count = 0
        for session_id, session in self.active_sessions.items():
            if session.get('user_id') == user_id:
                count += len(self.session_metrics.get(session_id, []))
        return count

    def get_real_time_engagement_metrics(self, user_id: str) -> Dict[str, Any]:
        """Get real-time engagement metrics for a user"""
        engagement_metrics = {
            'user_id': user_id,
            'active_sessions': 0,
            'total_turns_today': 0,
            'average_response_time': 0,
            'average_typing_speed': 0,
            'engagement_score': 0.0,
            'last_activity': 0,
            'session_duration': 0
        }
        
        current_time = int(time.time() * 1000)
        today_start = current_time - (24 * 60 * 60 * 1000)  # 24 hours ago
        
        for session_id, session in self.active_sessions.items():
            if session.get('user_id') == user_id:
                engagement_metrics['active_sessions'] += 1
                engagement_metrics['session_duration'] += (current_time - session['start_time'])
                
                # Count turns today
                session_turns = len([m for m in self.session_metrics.get(session_id, []) 
                                   if m.get('timestamp', 0) > today_start])
                engagement_metrics['total_turns_today'] += session_turns
                
                # Update last activity
                if session['last_activity'] > engagement_metrics['last_activity']:
                    engagement_metrics['last_activity'] = session['last_activity']
        
        # Calculate engagement score (0-100)
        if engagement_metrics['active_sessions'] > 0:
            # Base score from active sessions
            engagement_metrics['engagement_score'] = min(100, engagement_metrics['active_sessions'] * 20)
            
            # Bonus for recent activity
            if engagement_metrics['last_activity'] > 0:
                time_since_last = current_time - engagement_metrics['last_activity']
                if time_since_last < 5 * 60 * 1000:  # Less than 5 minutes
                    engagement_metrics['engagement_score'] += 20
                elif time_since_last < 30 * 60 * 1000:  # Less than 30 minutes
                    engagement_metrics['engagement_score'] += 10
            
            # Bonus for high turn count
            if engagement_metrics['total_turns_today'] > 10:
                engagement_metrics['engagement_score'] += 20
            elif engagement_metrics['total_turns_today'] > 5:
                engagement_metrics['engagement_score'] += 10
        
        return engagement_metrics

    def get_user_behavior_analysis(self, user_id: str) -> Dict[str, Any]:
        """Analyze user behavior patterns across all sessions"""
        behavior_analysis = {
            'user_id': user_id,
            'typing_patterns': {},
            'response_patterns': {},
            'engagement_patterns': {},
            'preferences': {},
            'anomalies': []
        }
        
        all_user_sessions = []
        for session_id, session in self.active_sessions.items():
            if session.get('user_id') == user_id:
                all_user_sessions.append(session_id)
        
        # Analyze typing patterns
        typing_durations = []
        message_lengths = []
        response_times = []
        
        for session_id in all_user_sessions:
            session_data = self.session_metrics.get(session_id, [])
            for metric in session_data:
                if metric.get('type') == 'user_prompt':
                    extracted = metric.get('extracted_metrics', {})
                    if extracted.get('typing_duration', 0) > 0:
                        typing_durations.append(extracted['typing_duration'])
                    if extracted.get('message_length', 0) > 0:
                        message_lengths.append(extracted['message_length'])
        
        # Calculate typing patterns
        if typing_durations:
            behavior_analysis['typing_patterns'] = {
                'average_typing_duration': sum(typing_durations) / len(typing_durations),
                'fastest_typing': min(typing_durations),
                'slowest_typing': max(typing_durations),
                'typing_consistency': 1.0 - (max(typing_durations) - min(typing_durations)) / max(typing_durations) if max(typing_durations) > 0 else 0
            }
        
        if message_lengths:
            behavior_analysis['typing_patterns']['message_lengths'] = {
                'average_length': sum(message_lengths) / len(message_lengths),
                'shortest_message': min(message_lengths),
                'longest_message': max(message_lengths),
                'length_variability': len(set(message_lengths)) / len(message_lengths)
            }
        
        # Detect anomalies
        if typing_durations and message_lengths:
            avg_typing = sum(typing_durations) / len(typing_durations)
            avg_length = sum(message_lengths) / len(message_lengths)
            
            for i, duration in enumerate(typing_durations):
                if duration > avg_typing * 3:  # 3x slower than average
                    behavior_analysis['anomalies'].append({
                        'type': 'slow_typing',
                        'session_index': i,
                        'duration': duration,
                        'expected': avg_typing
                    })
        
        return behavior_analysis

    def get_comprehensive_user_metrics(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive metrics for a user including real-time and historical data"""
        comprehensive_metrics = {
            'user_id': user_id,
            'timestamp': datetime.utcnow().isoformat(),
            'real_time': self.get_real_time_engagement_metrics(user_id),
            'behavior': self.get_user_behavior_analysis(user_id),
            'summary': {
                'total_sessions': 0,
                'total_interactions': 0,
                'average_session_duration': 0,
                'feedback_ratio': 0,
                'positive_feedback_ratio': 0
            }
        }
        
        # Calculate summary metrics
        user_sessions = [s for s in self.active_sessions.values() if s.get('user_id') == user_id]
        comprehensive_metrics['summary']['total_sessions'] = len(user_sessions)
        
        total_interactions = 0
        total_duration = 0
        feedback_count = 0
        positive_feedback_count = 0
        
        for session in user_sessions:
            session_id = session.get('session_id', '')
            if session_id in self.session_metrics:
                session_data = self.session_metrics[session_id]
                total_interactions += len(session_data)
                
                for metric in session_data:
                    if metric.get('type') == 'feedback':
                        feedback_count += 1
                        if metric.get('feedback_type') == 'positive':
                            positive_feedback_count += 1
                
                if session.get('start_time') and session.get('last_activity'):
                    total_duration += (session['last_activity'] - session['start_time'])
        
        comprehensive_metrics['summary']['total_interactions'] = total_interactions
        if user_sessions:
            comprehensive_metrics['summary']['average_session_duration'] = total_duration / len(user_sessions)
        
        if total_interactions > 0:
            comprehensive_metrics['summary']['feedback_ratio'] = feedback_count / total_interactions
        
        if feedback_count > 0:
            comprehensive_metrics['summary']['positive_feedback_ratio'] = positive_feedback_count / feedback_count
        
        return comprehensive_metrics

    def get_active_sessions(self) -> Dict[str, Dict[str, Any]]:
        """Get all active sessions"""
        return self.active_sessions.copy()

    def save_metrics_to_file(self, filepath: str):
        """Save all metrics to a JSON file"""
        data = {
            'timestamp': datetime.utcnow().isoformat(),
            'active_sessions': self.active_sessions,
            'session_metrics': self.session_metrics,
            'user_metrics': self.user_metrics
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2) 