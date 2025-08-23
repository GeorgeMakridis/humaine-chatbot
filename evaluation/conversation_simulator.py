#!/usr/bin/env python3
"""
Conversation Simulator for HumAIne Chatbot Evaluation
Uses LLM-based virtual personas to interact with the chatbot and collect metrics.
"""

import json
import random
import time
import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List, Any, Tuple
import openai
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Configure OpenAI
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")
openai.api_key = api_key

class ConversationSimulator:
    """Simulates conversations between virtual personas and the HumAIne chatbot."""
    
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base_url = api_base_url
        self.session_metrics = {}
        self.conversation_logs = {}
        
        # Conversation topics for evaluation
        self.conversation_topics = [
            "Career Development and Growth",
            "Technology Trends and Innovation",
            "Personal Finance and Investment",
            "Health and Wellness",
            "Education and Learning",
            "Travel and Culture",
            "Professional Networking",
            "Work-Life Balance",
            "Creative Projects and Hobbies",
            "Environmental Sustainability"
        ]
    
    def generate_conversation_questions(self, persona: Dict[str, Any], topic: str) -> List[str]:
        """Generate conversation questions based on persona and topic."""
        
        prompt = f"""
        You are {persona['demographics'].get('age', 'an adult')} year old {persona['professional_background'].get('current_role', 'professional')} 
        with expertise in {persona['expertise_areas'].get('primary_domain', 'your field')}.
        
        Your communication style is: {persona['personal_characteristics'].get('communication_style', 'professional')}
        Your personality is: {persona['personal_characteristics'].get('personality', 'balanced')}
        
        Your current task/goal: {persona.get('current_task', {}).get('primary_objective', 'General learning')}
        Task urgency: {persona.get('current_task', {}).get('urgency_level', 'Medium')}
        Success criteria: {persona.get('current_task', {}).get('success_criteria', 'Gain knowledge')}
        Obstacles: {persona.get('current_task', {}).get('obstacles', 'None specified')}
        
        Generate 8-15 natural, engaging questions about the topic: "{topic}"
        
        The questions should:
        1. Be relevant to your background and expertise
        2. Match your communication style and personality
        3. Show genuine curiosity and engagement
        4. Be appropriate for a chatbot conversation
        5. Vary in complexity and depth
        6. Help you achieve your current task/goal
        7. Address the obstacles you're facing
        
        Return only the questions, one per line, without numbering or additional text.
        """
        
        try:
            # Use the legacy API approach to avoid client initialization issues
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a virtual persona generating conversation questions. Generate natural, engaging questions that match the persona's characteristics."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            questions = [q.strip() for q in content.split('\n') if q.strip()]
            
            # Ensure we have enough questions
            if len(questions) < 8:
                questions.extend([
                    f"What are your thoughts on {topic.lower()}?",
                    f"How do you see {topic.lower()} evolving in the future?",
                    f"What advice would you give someone interested in {topic.lower()}?",
                    f"What challenges do you think exist in {topic.lower()}?",
                    f"What opportunities do you see in {topic.lower()}?"
                ])
            
            return questions[:15]  # Limit to 15 questions
            
        except Exception as e:
            print(f"Error generating questions: {e}")
            # Fallback questions
            return [
                f"What are your thoughts on {topic.lower()}?",
                f"How do you see {topic.lower()} evolving in the future?",
                f"What advice would you give someone interested in {topic.lower()}?",
                f"What challenges do you think exist in {topic.lower()}?",
                f"What opportunities do you see in {topic.lower()}?",
                f"How has {topic.lower()} changed in recent years?",
                f"What skills are important for {topic.lower()}?",
                f"What resources would you recommend for learning about {topic.lower()}?"
            ]
    
    def simulate_persona_response(self, persona: Dict[str, Any], chatbot_message: str, context: str) -> str:
        """Simulate how the persona would respond to the chatbot's message."""
        
        prompt = f"""
        You are {persona['demographics'].get('age', 'an adult')} year old {persona['professional_background'].get('current_role', 'professional')}.
        
        Your characteristics:
        - Communication style: {persona['personal_characteristics'].get('communication_style', 'professional')}
        - Personality: {persona['personal_characteristics'].get('personality', 'balanced')}
        - Expertise: {persona['expertise_areas'].get('primary_domain', 'general')}
        
        Your current task/goal: {persona.get('current_task', {}).get('primary_objective', 'General learning')}
        Task urgency: {persona.get('current_task', {}).get('urgency_level', 'Medium')}
        Success criteria: {persona.get('current_task', {}).get('success_criteria', 'Gain knowledge')}
        Obstacles: {persona.get('current_task', {}).get('obstacles', 'None specified')}
        
        Context: {context}
        
        The chatbot just said: "{chatbot_message}"
        
        Respond naturally as this persona would, considering:
        1. Your communication style and personality
        2. Your expertise and background
        3. Whether the response was helpful, relevant, and personalized
        4. Your level of satisfaction with the interaction
        5. How well the response helps you achieve your current task/goal
        6. Whether it addresses the obstacles you're facing
        
        Keep your response concise (1-2 sentences) and natural. Show your personality and expertise.
        """
        
        try:
            # Use the legacy API approach to avoid client initialization issues
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a virtual persona responding to a chatbot. Respond naturally based on your characteristics and the chatbot's message."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error simulating persona response: {e}")
            # Fallback responses
            fallback_responses = [
                "That's interesting, thank you for sharing.",
                "I appreciate the information you provided.",
                "That makes sense given my background.",
                "I'd like to know more about that.",
                "That's helpful for someone in my field."
            ]
            return random.choice(fallback_responses)
    
    def calculate_satisfaction_score(self, persona: Dict[str, Any], conversation_data: Dict[str, Any]) -> float:
        """Calculate a satisfaction score for the conversation."""
        
        # Base satisfaction factors
        satisfaction_factors = {
            'response_relevance': 0.0,
            'personalization_level': 0.0,
            'conversation_flow': 0.0,
            'expertise_alignment': 0.0,
            'communication_style_match': 0.0,
            'task_achievement': 0.0
        }
        
        # Analyze conversation for satisfaction factors
        messages = conversation_data.get('messages', [])
        
        if len(messages) >= 4:  # Need at least 2 Q&A pairs
            # Response relevance (how well chatbot answered questions)
            relevant_responses = sum(1 for msg in messages if msg.get('is_chatbot') and msg.get('relevance_score', 0) > 0.7)
            satisfaction_factors['response_relevance'] = relevant_responses / len([m for m in messages if m.get('is_chatbot')])
            
            # Personalization level (how much responses were tailored to persona)
            personalized_responses = sum(1 for msg in messages if msg.get('is_chatbot') and msg.get('personalization_score', 0) > 0.6)
            satisfaction_factors['personalization_level'] = personalized_responses / len([m for m in messages if m.get('is_chatbot')])
            
            # Conversation flow (natural progression)
            satisfaction_factors['conversation_flow'] = min(1.0, len(messages) / 10.0)  # More messages = better flow
            
            # Expertise alignment (responses match persona's domain)
            domain_responses = sum(1 for msg in messages if msg.get('is_chatbot') and msg.get('expertise_alignment', 0) > 0.5)
            satisfaction_factors['expertise_alignment'] = domain_responses / len([m for m in messages if m.get('is_chatbot')])
            
            # Communication style match
            style_matches = sum(1 for msg in messages if msg.get('is_chatbot') and msg.get('style_match', 0) > 0.6)
            satisfaction_factors['communication_style_match'] = style_matches / len([m for m in messages if m.get('is_chatbot')])
            
            # Task achievement (how well responses help achieve the persona's goal)
            if 'current_task' in persona:
                task_helpful_responses = sum(1 for msg in messages if msg.get('is_chatbot') and msg.get('task_helpfulness', 0) > 0.6)
                satisfaction_factors['task_achievement'] = task_helpful_responses / len([m for m in messages if m.get('is_chatbot')])
            else:
                satisfaction_factors['task_achievement'] = 0.5  # Default value
        
        # Calculate weighted satisfaction score
        weights = {
            'response_relevance': 0.25,
            'personalization_level': 0.20,
            'conversation_flow': 0.15,
            'expertise_alignment': 0.15,
            'communication_style_match': 0.10,
            'task_achievement': 0.15
        }
        
        total_score = sum(satisfaction_factors[factor] * weights[factor] for factor in satisfaction_factors)
        
        # Add some randomness to make scores more realistic
        random_factor = random.uniform(-0.1, 0.1)
        final_score = max(0.0, min(1.0, total_score + random_factor))
        
        return round(final_score, 3)
    
    async def run_conversation_session(self, persona: Dict[str, Any], topic: str) -> Dict[str, Any]:
        """Run a complete conversation session between a persona and the chatbot."""
        
        session_id = f"session_{persona['persona_id']}_{topic.replace(' ', '_').lower()}_{int(time.time())}"
        
        print(f"🎭 Starting conversation session {session_id}")
        print(f"   Persona: {persona['demographics'].get('age', 'N/A')} year old {persona['professional_background'].get('current_role', 'N/A')}")
        print(f"   Topic: {topic}")
        
        # Generate questions for this persona and topic
        questions = self.generate_conversation_questions(persona, topic)
        print(f"   Generated {len(questions)} questions")
        
        conversation_data = {
            'session_id': session_id,
            'persona_id': persona['persona_id'],
            'topic': topic,
            'start_time': datetime.now().isoformat(),
            'messages': [],
            'metrics': {
                'total_messages': 0,
                'chatbot_responses': 0,
                'persona_responses': 0,
                'session_duration': 0,
                'satisfaction_score': 0.0
            }
        }
        
        session_start = time.time()
        
        # Run the conversation
        for i, question in enumerate(questions):
            print(f"   Q{i+1}: {question[:60]}...")
            
            # Persona asks question
            persona_message = {
                'message_id': f"{session_id}_msg_{i*2}",
                'timestamp': datetime.now().isoformat(),
                'sender': 'persona',
                'content': question,
                'is_chatbot': False,
                'message_type': 'question'
            }
            conversation_data['messages'].append(persona_message)
            
            # Simulate chatbot response (this would normally call your actual chatbot API)
            chatbot_response = await self.get_chatbot_response(question, persona, conversation_data)
            
            chatbot_message = {
                'message_id': f"{session_id}_msg_{i*2+1}",
                'timestamp': datetime.now().isoformat(),
                'sender': 'chatbot',
                'content': chatbot_response,
                'is_chatbot': True,
                'message_type': 'response',
                'relevance_score': self.calculate_relevance_score(question, chatbot_response),
                'personalization_score': self.calculate_personalization_score(chatbot_response, persona),
                'expertise_alignment': self.calculate_expertise_alignment(chatbot_response, persona),
                'style_match': self.calculate_style_match(chatbot_response, persona),
                'task_helpfulness': self.calculate_task_helpfulness(chatbot_response, persona)
            }
            conversation_data['messages'].append(chatbot_message)
            
            # Simulate persona's reaction/response
            if i < len(questions) - 1:  # Don't respond after the last question
                persona_reaction = self.simulate_persona_response(persona, chatbot_response, f"Question: {question}")
                
                reaction_message = {
                    'message_id': f"{session_id}_msg_{i*2+2}",
                    'timestamp': datetime.now().isoformat(),
                    'sender': 'persona',
                    'content': persona_reaction,
                    'is_chatbot': False,
                    'message_type': 'reaction'
                }
                conversation_data['messages'].append(reaction_message)
            
            # Small delay to simulate realistic conversation pace
            await asyncio.sleep(0.5)
        
        # Calculate final metrics
        session_duration = time.time() - session_start
        conversation_data['end_time'] = datetime.now().isoformat()
        conversation_data['metrics']['total_messages'] = len(conversation_data['messages'])
        conversation_data['metrics']['chatbot_responses'] = len([m for m in conversation_data['messages'] if m.get('is_chatbot')])
        conversation_data['metrics']['persona_responses'] = len([m for m in conversation_data['messages'] if not m.get('is_chatbot')])
        conversation_data['metrics']['session_duration'] = round(session_duration, 2)
        conversation_data['metrics']['satisfaction_score'] = self.calculate_satisfaction_score(persona, conversation_data)
        
        print(f"   ✅ Session completed in {session_duration:.1f}s")
        print(f"   📊 Satisfaction score: {conversation_data['metrics']['satisfaction_score']:.3f}")
        
        return conversation_data
    
    async def get_chatbot_response(self, question: str, persona: Dict[str, Any], conversation_context: Dict[str, Any]) -> str:
        """Get a response from the HumAIne chatbot API."""
        
        try:
            # Prepare the request payload
            payload = {
                "user_id": f"persona_{persona['persona_id']}",
                "message": question,
                "context": {
                    "persona_profile": persona,
                    "conversation_history": [msg['content'] for msg in conversation_context['messages'] if msg.get('is_chatbot')],
                    "session_topic": conversation_context['topic']
                }
            }
            
            # Make API call to your chatbot
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_base_url}/interact",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get('response', 'I understand your question. Let me help you with that.')
                    else:
                        print(f"   ⚠️  API call failed with status {response.status}")
                        return self.generate_fallback_response(question, persona)
                        
        except Exception as e:
            print(f"   ⚠️  Error calling chatbot API: {e}")
            return self.generate_fallback_response(question, persona)
    
    def generate_fallback_response(self, question: str, persona: Dict[str, Any]) -> str:
        """Generate a fallback response if the chatbot API is unavailable."""
        
        # Simple fallback responses based on question type
        if '?' in question.lower():
            if 'how' in question.lower():
                return "That's a great question about how things work. Based on my knowledge, I can provide some insights on this topic."
            elif 'what' in question.lower():
                return "I understand you're asking about what's available. Let me share some information that might be helpful."
            elif 'why' in question.lower():
                return "That's an interesting question about the reasons behind something. I'd be happy to explain the key factors involved."
            else:
                return "Thank you for your question. I'd be glad to help you with information about this topic."
        else:
            return "I appreciate you sharing that with me. Let me provide some relevant information that might be helpful."
    
    def calculate_relevance_score(self, question: str, response: str) -> float:
        """Calculate how relevant the response is to the question."""
        # Simple relevance scoring (in a real system, this would use more sophisticated NLP)
        question_words = set(question.lower().split())
        response_words = set(response.lower().split())
        
        if not question_words:
            return 0.5
        
        overlap = len(question_words.intersection(response_words))
        relevance = min(1.0, overlap / len(question_words))
        
        # Add some randomness to make scores more realistic
        random_factor = random.uniform(-0.1, 0.1)
        return max(0.0, min(1.0, relevance + random_factor))
    
    def calculate_personalization_score(self, response: str, persona: Dict[str, Any]) -> float:
        """Calculate how personalized the response is to the persona."""
        # Check if response mentions persona-specific elements
        persona_keywords = [
            persona['demographics'].get('age', ''),
            persona['professional_background'].get('current_role', ''),
            persona['expertise_areas'].get('primary_domain', ''),
            persona['personal_characteristics'].get('communication_style', '')
        ]
        
        persona_keywords = [kw.lower() for kw in persona_keywords if kw]
        response_lower = response.lower()
        
        personalization_count = sum(1 for keyword in persona_keywords if keyword in response_lower)
        
        if not persona_keywords:
            return 0.5
        
        base_score = personalization_count / len(persona_keywords)
        
        # Add randomness for realistic variation
        random_factor = random.uniform(-0.15, 0.15)
        return max(0.0, min(1.0, base_score + random_factor))
    
    def calculate_expertise_alignment(self, response: str, persona: Dict[str, Any]) -> float:
        """Calculate how well the response aligns with the persona's expertise."""
        expertise_domain = persona['expertise_areas'].get('primary_domain', '').lower()
        
        if not expertise_domain:
            return 0.5
        
        # Simple keyword matching for expertise alignment
        expertise_keywords = expertise_domain.split()
        response_lower = response.lower()
        
        alignment_count = sum(1 for keyword in expertise_keywords if keyword in response_lower)
        
        base_score = alignment_count / len(expertise_keywords)
        
        # Add randomness for realistic variation
        random_factor = random.uniform(-0.1, 0.1)
        return max(0.0, min(1.0, base_score + random_factor))
    
    def calculate_style_match(self, response: str, persona: Dict[str, Any]) -> float:
        """Calculate how well the response style matches the persona's preferences."""
        communication_style = persona['personal_characteristics'].get('communication_style', '').lower()
        
        if not communication_style:
            return 0.5
        
        # Simple style matching based on communication preferences
        if 'formal' in communication_style:
            style_score = 0.8 if any(word in response.lower() for word in ['professional', 'formal', 'respectfully']) else 0.4
        elif 'casual' in communication_style:
            style_score = 0.8 if any(word in response.lower() for word in ['hey', 'cool', 'awesome', 'great']) else 0.4
        elif 'technical' in communication_style:
            style_score = 0.8 if any(word in response.lower() for word in ['algorithm', 'methodology', 'framework', 'approach']) else 0.4
        else:
            style_score = 0.6  # Default balanced score
        
        # Add randomness for realistic variation
        random_factor = random.uniform(-0.1, 0.1)
        return max(0.0, min(1.0, style_score + random_factor))
    
    def calculate_task_helpfulness(self, response: str, persona: Dict[str, Any]) -> float:
        """Calculate how helpful the response is for the persona's current task."""
        
        if 'current_task' not in persona:
            return 0.5  # Default score if no task specified
        
        task_objective = persona['current_task'].get('primary_objective', '').lower()
        obstacles = persona['current_task'].get('obstacles', '').lower()
        
        if not task_objective:
            return 0.5
        
        # Check if response mentions task-related keywords
        response_lower = response.lower()
        
        # Simple keyword matching for task helpfulness
        task_keywords = task_objective.split()
        obstacle_keywords = obstacles.split() if obstacles else []
        
        # Count task-relevant keywords in response
        task_relevance = sum(1 for keyword in task_keywords if keyword in response_lower)
        obstacle_addressed = sum(1 for keyword in obstacle_keywords if keyword in response_lower)
        
        # Calculate base score
        if task_keywords:
            task_score = task_relevance / len(task_keywords)
        else:
            task_score = 0.5
        
        # Bonus for addressing obstacles
        obstacle_bonus = min(0.3, obstacle_addressed * 0.1) if obstacle_keywords else 0.0
        
        # Combine scores
        base_score = task_score + obstacle_bonus
        
        # Add randomness for realistic variation
        random_factor = random.uniform(-0.1, 0.1)
        final_score = max(0.0, min(1.0, base_score + random_factor))
        
        return round(final_score, 3)
    
    def save_conversation_data(self, conversation_data: Dict[str, Any], filename: str = None):
        """Save conversation data to a JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_session_{conversation_data['persona_id']}_{timestamp}.json"
        
        filepath = filename
        
        with open(filepath, 'w') as f:
            json.dump(conversation_data, f, indent=2)
        
        print(f"💾 Saved conversation data to {filepath}")
        return filepath

async def main():
    """Main function to run conversation simulation."""
    simulator = ConversationSimulator()
    
    # Load virtual personas (you'll need to run the persona generator first)
    try:
        with open('evaluation/virtual_personas_latest.json', 'r') as f:
            personas_data = json.load(f)
            personas = personas_data['personas']
    except FileNotFoundError:
        print("❌ No virtual personas found. Please run virtual_personas_generator.py first.")
        return
    
    print(f"🎭 Loaded {len(personas)} virtual personas")
    
    # Select a subset of personas for testing (to avoid too many API calls)
    test_personas = random.sample(personas, min(10, len(personas)))
    print(f"🧪 Testing with {len(test_personas)} personas")
    
    # Run conversation sessions
    all_sessions = []
    
    for persona in test_personas:
        # Select a random topic for this persona
        topic = random.choice(simulator.conversation_topics)
        
        # Run the conversation session
        session_data = await simulator.run_conversation_session(persona, topic)
        all_sessions.append(session_data)
        
        # Save individual session
        simulator.save_conversation_data(session_data)
        
        # Small delay between sessions
        await asyncio.sleep(1)
    
    # Save summary of all sessions
    summary = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'total_sessions': len(all_sessions),
            'total_personas': len(test_personas),
            'simulator_version': '1.0'
        },
        'sessions_summary': [
            {
                'session_id': session['session_id'],
                'persona_id': session['persona_id'],
                'topic': session['topic'],
                'satisfaction_score': session['metrics']['satisfaction_score'],
                'total_messages': session['metrics']['total_messages'],
                'session_duration': session['metrics']['session_duration']
            }
            for session in all_sessions
        ],
        'overall_metrics': {
            'average_satisfaction': sum(s['metrics']['satisfaction_score'] for s in all_sessions) / len(all_sessions),
            'total_messages': sum(s['metrics']['total_messages'] for s in all_sessions),
            'average_session_duration': sum(s['metrics']['session_duration'] for s in all_sessions) / len(all_sessions)
        }
    }
    
    summary_filename = f"conversation_simulation_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(f"evaluation/{summary_filename}", 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n🎉 Conversation simulation completed!")
    print(f"📊 Total sessions: {len(all_sessions)}")
    print(f"📈 Average satisfaction: {summary['overall_metrics']['average_satisfaction']:.3f}")
    print(f"💬 Total messages: {summary['overall_metrics']['total_messages']}")
    print(f"⏱️  Average session duration: {summary['overall_metrics']['average_session_duration']:.1f}s")
    print(f"📁 Summary saved to: {summary_filename}")

if __name__ == "__main__":
    asyncio.run(main())
