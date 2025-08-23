"""
User Study Simulation for HumAIne-chatbot

This script simulates the user study described in the research paper,
demonstrating the personalized chatbot system with different user types.
"""

import time
import json
import random
from typing import Dict, Any, List
from datetime import datetime

from src.core.dialogue_manager import DialogueManager


class UserStudySimulator:
    """Simulates user study scenarios for HumAIne-chatbot"""
    
    def __init__(self):
        """Initialize the simulator"""
        self.dialogue_manager = DialogueManager()
        self.scenarios = self._load_scenarios()
        self.user_types = self._load_user_types()
    
    def _load_scenarios(self) -> List[Dict[str, Any]]:
        """Load predefined conversation scenarios"""
        return [
            {
                "id": "finance_advice",
                "name": "Personal Finance Advice",
                "description": "User asks for financial advice and investment recommendations",
                "messages": [
                    "I want to start investing but I'm not sure where to begin. Can you help me?",
                    "What are some good options for a beginner investor?",
                    "How much should I invest initially?",
                    "What about risk management?"
                ]
            },
            {
                "id": "technical_explanation",
                "name": "Technical Concept Explanation",
                "description": "User asks for explanation of a technical concept",
                "messages": [
                    "Can you explain machine learning in simple terms?",
                    "What's the difference between supervised and unsupervised learning?",
                    "How does a neural network work?",
                    "Can you give me some real-world examples?"
                ]
            },
            {
                "id": "healthcare_inquiry",
                "name": "Healthcare Information",
                "description": "User asks for health-related information",
                "messages": [
                    "What are the symptoms of seasonal allergies?",
                    "How can I improve my sleep quality?",
                    "What's a healthy diet for someone with diabetes?",
                    "Should I be concerned about these symptoms?"
                ]
            },
            {
                "id": "educational_help",
                "name": "Educational Assistance",
                "description": "User asks for help with learning a new subject",
                "messages": [
                    "I'm trying to learn Python programming. Where should I start?",
                    "What are the best resources for beginners?",
                    "How long does it take to become proficient?",
                    "Can you recommend some practice projects?"
                ]
            }
        ]
    
    def _load_user_types(self) -> List[Dict[str, Any]]:
        """Load different user types for simulation"""
        return [
            {
                "id": "technical_expert",
                "name": "Technical Expert",
                "description": "Highly technical user with advanced knowledge",
                "profile": {
                    "preferred_language_complexity": "complex",
                    "preferred_response_style": "professional",
                    "preferred_detail_level": "detailed",
                    "average_typing_speed": 8.0,
                    "average_sentiment_score": 1.0,
                    "average_language_complexity": 0.8,
                    "average_grammatical_accuracy": 0.98
                }
            },
            {
                "id": "casual_user",
                "name": "Casual User",
                "description": "Casual user with basic technical knowledge",
                "profile": {
                    "preferred_language_complexity": "simple",
                    "preferred_response_style": "conversational",
                    "preferred_detail_level": "concise",
                    "average_typing_speed": 4.0,
                    "average_sentiment_score": 2.0,
                    "average_language_complexity": 0.4,
                    "average_grammatical_accuracy": 0.85
                }
            },
            {
                "id": "professional_user",
                "name": "Professional User",
                "description": "Professional user with moderate technical knowledge",
                "profile": {
                    "preferred_language_complexity": "medium",
                    "preferred_response_style": "balanced",
                    "preferred_detail_level": "medium",
                    "average_typing_speed": 6.0,
                    "average_sentiment_score": 0.5,
                    "average_language_complexity": 0.6,
                    "average_grammatical_accuracy": 0.92
                }
            },
            {
                "id": "student_user",
                "name": "Student User",
                "description": "Student learning new concepts",
                "profile": {
                    "preferred_language_complexity": "medium",
                    "preferred_response_style": "enthusiastic",
                    "preferred_detail_level": "detailed",
                    "average_typing_speed": 5.0,
                    "average_sentiment_score": 1.5,
                    "average_language_complexity": 0.5,
                    "average_grammatical_accuracy": 0.88
                }
            }
        ]
    
    def simulate_user_study(self, num_participants: int = 10) -> Dict[str, Any]:
        """Simulate a complete user study"""
        print("Starting HumAIne-chatbot User Study Simulation")
        print("=" * 50)
        
        results = {
            "study_info": {
                "participants": num_participants,
                "start_time": datetime.utcnow().isoformat(),
                "scenarios": len(self.scenarios),
                "user_types": len(self.user_types)
            },
            "participants": [],
            "overall_metrics": {}
        }
        
        for participant_id in range(num_participants):
            print(f"\nParticipant {participant_id + 1}/{num_participants}")
            print("-" * 30)
            
            # Select random user type and scenario
            user_type = random.choice(self.user_types)
            scenario = random.choice(self.scenarios)
            
            participant_result = self._simulate_participant(
                participant_id, user_type, scenario
            )
            
            results["participants"].append(participant_result)
        
        # Calculate overall metrics
        results["overall_metrics"] = self._calculate_overall_metrics(results["participants"])
        
        # Save results
        self._save_study_results(results)
        
        print("\n" + "=" * 50)
        print("User Study Simulation Complete!")
        print(f"Results saved to: data/user_sessions/study_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        return results
    
    def _simulate_participant(self, participant_id: int, user_type: Dict[str, Any], 
                             scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate a single participant"""
        user_id = f"participant_{participant_id:03d}_{user_type['id']}"
        
        print(f"User Type: {user_type['name']}")
        print(f"Scenario: {scenario['name']}")
        
        # Create user profile
        profile = self.dialogue_manager.user_profiler.create_user_profile(user_id)
        
        # Set profile attributes based on user type
        for key, value in user_type["profile"].items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        # Start conversation
        session_id = self.dialogue_manager.start_conversation(user_id)
        
        conversation_log = []
        feedback_log = []
        
        # Simulate conversation
        for i, message in enumerate(scenario["messages"]):
            print(f"  Turn {i + 1}: {message[:50]}...")
            
            # Simulate typing times
            typing_start = int(time.time() * 1000)
            time.sleep(random.uniform(1, 3))  # Simulate thinking time
            typing_end = int(time.time() * 1000)
            
            # Send message
            response, metadata = self.dialogue_manager.process_user_message(
                session_id, message, typing_start, typing_end
            )
            
            conversation_log.append({
                "turn": i + 1,
                "user_message": message,
                "bot_response": response,
                "metadata": metadata
            })
            
            # Simulate feedback (70% chance of positive feedback for good responses)
            if random.random() < 0.7:
                feedback_type = "positive"
            else:
                feedback_type = "negative"
            
            # Record feedback
            feedback_data = self.dialogue_manager.record_feedback(
                session_id, response, typing_end, int(time.time() * 1000), feedback_type
            )
            
            feedback_log.append({
                "turn": i + 1,
                "feedback_type": feedback_type,
                "feedback_data": feedback_data
            })
            
            time.sleep(random.uniform(1, 2))  # Pause between turns
        
        # End conversation
        session_data = self.dialogue_manager.end_conversation(session_id, "taskCompletion")
        
        # Get final user profile
        final_profile = self.dialogue_manager.get_user_profile(user_id)
        
        participant_result = {
            "participant_id": participant_id,
            "user_id": user_id,
            "user_type": user_type,
            "scenario": scenario,
            "conversation_log": conversation_log,
            "feedback_log": feedback_log,
            "session_data": session_data.dict() if session_data else None,
            "final_profile": final_profile.dict() if final_profile else None,
            "personalization_params": self.dialogue_manager.get_personalization_parameters(user_id)
        }
        
        print(f"  Completed: {len(conversation_log)} turns, {len(feedback_log)} feedback instances")
        
        return participant_result
    
    def _calculate_overall_metrics(self, participants: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate overall study metrics"""
        total_turns = sum(len(p["conversation_log"]) for p in participants)
        total_feedback = sum(len(p["feedback_log"]) for p in participants)
        positive_feedback = sum(
            1 for p in participants 
            for f in p["feedback_log"] 
            if f["feedback_type"] == "positive"
        )
        
        # Calculate average session duration
        session_durations = [
            p["session_data"]["session_duration"] 
            for p in participants 
            if p["session_data"]
        ]
        
        avg_session_duration = sum(session_durations) / len(session_durations) if session_durations else 0
        
        # Calculate engagement metrics
        engagement_ratios = [
            p["session_data"]["engagement"]["engagement_time"] / p["session_data"]["session_duration"]
            for p in participants 
            if p["session_data"] and p["session_data"]["session_duration"] > 0
        ]
        
        avg_engagement = sum(engagement_ratios) / len(engagement_ratios) if engagement_ratios else 0
        
        return {
            "total_participants": len(participants),
            "total_turns": total_turns,
            "total_feedback": total_feedback,
            "positive_feedback_count": positive_feedback,
            "positive_feedback_ratio": positive_feedback / total_feedback if total_feedback > 0 else 0,
            "average_session_duration": avg_session_duration,
            "average_engagement": avg_engagement,
            "average_turns_per_session": total_turns / len(participants) if participants else 0
        }
    
    def _save_study_results(self, results: Dict[str, Any]):
        """Save study results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/user_sessions/study_results_{timestamp}.json"
        
        # Ensure directory exists
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
    
    def print_study_summary(self, results: Dict[str, Any]):
        """Print a summary of the study results"""
        metrics = results["overall_metrics"]
        
        print("\n" + "=" * 50)
        print("USER STUDY SUMMARY")
        print("=" * 50)
        print(f"Total Participants: {metrics['total_participants']}")
        print(f"Total Conversation Turns: {metrics['total_turns']}")
        print(f"Total Feedback Instances: {metrics['total_feedback']}")
        print(f"Positive Feedback Rate: {metrics['positive_feedback_ratio']:.2%}")
        print(f"Average Session Duration: {metrics['average_session_duration'] / 1000:.1f} seconds")
        print(f"Average Engagement: {metrics['average_engagement']:.2%}")
        print(f"Average Turns per Session: {metrics['average_turns_per_session']:.1f}")
        
        # User type breakdown
        user_type_counts = {}
        for participant in results["participants"]:
            user_type = participant["user_type"]["id"]
            user_type_counts[user_type] = user_type_counts.get(user_type, 0) + 1
        
        print("\nUser Type Distribution:")
        for user_type, count in user_type_counts.items():
            print(f"  {user_type}: {count} participants")
        
        # Scenario breakdown
        scenario_counts = {}
        for participant in results["participants"]:
            scenario = participant["scenario"]["id"]
            scenario_counts[scenario] = scenario_counts.get(scenario, 0) + 1
        
        print("\nScenario Distribution:")
        for scenario, count in scenario_counts.items():
            print(f"  {scenario}: {count} participants")


def main():
    """Main function to run the user study simulation"""
    simulator = UserStudySimulator()
    
    # Run simulation with 20 participants
    results = simulator.simulate_user_study(num_participants=20)
    
    # Print summary
    simulator.print_study_summary(results)


if __name__ == "__main__":
    main() 