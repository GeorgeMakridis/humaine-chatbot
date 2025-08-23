"""
OpenAI Integration for HumAIne-chatbot

This module provides OpenAI API integration that tailors requests based on
user profiling and personalization parameters.
"""

import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

try:
    from openai import OpenAI
except ImportError:
    print("⚠️  OpenAI library not installed. Using mock responses.")
    OpenAI = None


class OpenAIIntegration:
    """OpenAI API integration with user profiling"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI integration
        
        Args:
            api_key: OpenAI API key (if None, will try to get from environment)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = None
        
        if OpenAI and self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
                print("✅ OpenAI client initialized successfully")
            except Exception as e:
                print(f"⚠️  Failed to initialize OpenAI client: {e}")
                self.client = None
        else:
            print("⚠️  OpenAI client not available - using mock responses")
    
    async def generate_response(self, 
                         user_message: str,
                         personalization_params: Dict[str, Any],
                         conversation_history: Optional[List[Dict[str, str]]] = None,
                         system_context: Optional[str] = None) -> str:
        """
        Generate personalized response using OpenAI API
        
        Args:
            user_message: The user's message
            personalization_params: User personalization parameters from profiler
            conversation_history: Previous conversation messages
            system_context: Additional system context
            
        Returns:
            Generated response tailored to user preferences
        """
        if not self.client:
            return self._generate_mock_response(user_message, personalization_params)
        
        try:
            # Build the system prompt based on personalization
            system_prompt = self._build_system_prompt(personalization_params, system_context)
            
            # Build the conversation messages
            messages = self._build_messages(user_message, system_prompt, conversation_history)
            
            # Set model parameters based on personalization
            model_params = self._get_model_parameters(personalization_params)
            
            # Make API call
            response = self.client.chat.completions.create(
                model=model_params.get('model', 'gpt-3.5-turbo'),
                messages=messages,
                max_tokens=model_params.get('max_tokens', 1000),
                temperature=model_params.get('temperature', 0.7),
                top_p=model_params.get('top_p', 1.0),
                frequency_penalty=model_params.get('frequency_penalty', 0.0),
                presence_penalty=model_params.get('presence_penalty', 0.0)
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"⚠️  OpenAI API error: {e}")
            return self._generate_mock_response(user_message, personalization_params)

    def generate_response_sync(self, 
                              user_message: str,
                              personalization_params: Dict[str, Any],
                              conversation_history: Optional[List[Dict[str, str]]] = None,
                              system_context: Optional[str] = None) -> str:
        """
        Synchronous version of generate_response for RL agent compatibility
        
        Args:
            user_message: The user's message
            personalization_params: User personalization parameters from profiler
            conversation_history: Previous conversation messages
            system_context: Optional system context
            
        Returns:
            Generated response tailored to user preferences
        """
        # For synchronous calls, use mock response to avoid async issues
        if not self.client:
            return self._generate_mock_response(user_message, personalization_params)
        
        try:
            # Build the system prompt based on personalization
            system_prompt = self._build_system_prompt(personalization_params, None)
            
            # Build the conversation messages
            messages = self._build_messages(user_message, system_prompt, conversation_history)
            
            # Set model parameters based on personalization
            model_params = self._get_model_parameters(personalization_params)
            
            # Make API call synchronously (this will block)
            response = self.client.chat.completions.create(
                model=model_params.get('model', 'gpt-3.5-turbo'),
                messages=messages,
                max_tokens=model_params.get('max_tokens', 1000),
                temperature=model_params.get('temperature', 0.7),
                top_p=model_params.get('top_p', 1.0),
                frequency_penalty=model_params.get('frequency_penalty', 0.0),
                presence_penalty=model_params.get('presence_penalty', 0.0)
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"⚠️  OpenAI API error in sync call: {e}")
            return self._generate_mock_response(user_message, personalization_params)

    def check_connectivity(self) -> Dict[str, Any]:
        """
        Check OpenAI API connectivity and return status
        
        Returns:
            Dictionary with connectivity status and details
        """
        if not self.client:
            return {
                "status": "disconnected",
                "reason": "No OpenAI client available",
                "api_key_present": bool(self.api_key),
                "openai_library": bool(OpenAI)
            }
        
        try:
            # Test with a simple API call
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            
            return {
                "status": "connected",
                "model": "gpt-3.5-turbo",
                "api_key_present": bool(self.api_key),
                "test_response": response.choices[0].message.content,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "api_key_present": bool(self.api_key),
                "openai_library": bool(OpenAI),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _build_system_prompt(self, personalization_params: Dict[str, Any], 
                            system_context: Optional[str] = None) -> str:
        """Build system prompt based on user personalization"""
        
        # Base system prompt
        base_prompt = "You are a helpful AI assistant."
        
        # Add personalization context
        language_complexity = personalization_params.get('language_complexity', 'medium')
        response_style = personalization_params.get('response_style', 'balanced')
        detail_level = personalization_params.get('detail_level', 'medium')
        user_type = personalization_params.get('user_type', 'general')
        engagement_level = personalization_params.get('engagement_level', 'medium')
        
        # Build personalization instructions
        instructions = []
        
        # Language complexity instructions
        if language_complexity == 'simple':
            instructions.append("Use simple vocabulary and short sentences. Avoid technical jargon.")
        elif language_complexity == 'complex':
            instructions.append("Use advanced vocabulary and detailed explanations. Include technical terms when appropriate.")
        else:
            instructions.append("Use standard vocabulary and balanced explanations.")
        
        # Response style instructions
        if response_style == 'conversational':
            instructions.append("Maintain a friendly and casual tone. Use conversational language.")
        elif response_style == 'professional':
            instructions.append("Maintain a formal and professional tone. Use business-appropriate language.")
        elif response_style == 'enthusiastic':
            instructions.append("Maintain an excited and motivational tone. Show enthusiasm in responses.")
        else:
            instructions.append("Maintain a balanced and neutral tone.")
        
        # Detail level instructions
        if detail_level == 'concise':
            instructions.append("Provide brief and direct answers. Focus on essential information.")
        elif detail_level == 'detailed':
            instructions.append("Provide comprehensive explanations with examples and context.")
        else:
            instructions.append("Provide balanced explanations with appropriate detail.")
        
        # User type specific instructions
        if user_type == 'technical_expert':
            instructions.append("This user has technical expertise. You can use advanced technical concepts.")
        elif user_type == 'casual_user':
            instructions.append("This user prefers casual conversation. Keep responses friendly and accessible.")
        elif user_type == 'professional_user':
            instructions.append("This user prefers professional communication. Maintain formal standards.")
        
        # Engagement level instructions
        if engagement_level == 'high':
            instructions.append("This user is highly engaged. Provide detailed and interactive responses.")
        elif engagement_level == 'low':
            instructions.append("This user may have limited engagement. Keep responses concise and clear.")
        
        # Combine all instructions
        personalization_text = " ".join(instructions)
        
        # Build final system prompt
        system_prompt = f"{base_prompt} {personalization_text}"
        
        if system_context:
            system_prompt += f" Additional context: {system_context}"
        
        return system_prompt
    
    def _build_messages(self, user_message: str, system_prompt: str,
                       conversation_history: Optional[List[Dict[str, str]]] = None) -> List[Dict[str, str]]:
        """Build messages for OpenAI API"""
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history if available
        if conversation_history:
            for msg in conversation_history[-10:]:  # Limit to last 10 messages
                messages.append({
                    "role": msg.get('role', 'user'),
                    "content": msg.get('content', '')
                })
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        return messages
    
    def _get_model_parameters(self, personalization_params: Dict[str, Any]) -> Dict[str, Any]:
        """Get model parameters based on personalization"""
        
        # Base parameters
        params = {
            'model': 'gpt-3.5-turbo',
            'temperature': 0.7,
            'max_tokens': 1000,
            'top_p': 1.0,
            'frequency_penalty': 0.0,
            'presence_penalty': 0.0
        }
        
        # Adjust based on user preferences
        detail_level = personalization_params.get('detail_level', 'medium')
        language_complexity = personalization_params.get('language_complexity', 'medium')
        response_style = personalization_params.get('response_style', 'balanced')
        
        # Adjust max_tokens based on detail level
        if detail_level == 'concise':
            params['max_tokens'] = 500
        elif detail_level == 'detailed':
            params['max_tokens'] = 1500
        
        # Adjust temperature based on response style
        if response_style == 'conversational':
            params['temperature'] = 0.8
        elif response_style == 'professional':
            params['temperature'] = 0.5
        elif response_style == 'enthusiastic':
            params['temperature'] = 0.9
        
        # Adjust for language complexity
        if language_complexity == 'complex':
            params['max_tokens'] = min(params['max_tokens'] + 200, 2000)
        
        return params
    
    def _generate_mock_response(self, user_message: str, 
                              personalization_params: Dict[str, Any]) -> str:
        """Generate mock response when OpenAI is not available"""
        
        response_style = personalization_params.get('response_style', 'balanced')
        detail_level = personalization_params.get('detail_level', 'medium')
        language_complexity = personalization_params.get('language_complexity', 'medium')
        
        # Generate more natural, conversational responses
        if "hi" in user_message.lower() or "hello" in user_message.lower() or "hey" in user_message.lower():
            return "Hi there! 👋 How can I help you today?"
        
        elif "how are you" in user_message.lower():
            return "I'm doing great, thanks for asking! 😊 What would you like to chat about?"
        
        elif "rich" in user_message.lower() or "money" in user_message.lower() or "wealth" in user_message.lower():
            if detail_level == 'concise':
                return "Building wealth takes time and smart choices. Focus on saving, investing, and developing valuable skills. What specific area interests you most?"
            elif detail_level == 'detailed':
                return "Great question! Building wealth involves several key strategies: 1) Save consistently (aim for 20% of income), 2) Invest in diversified assets, 3) Develop high-value skills, 4) Start a business if you're entrepreneurial, and 5) Avoid lifestyle inflation. Which of these areas would you like to explore further?"
            else:
                return "Building wealth is about smart financial habits. Start with saving, then learn about investing. What's your current financial situation?"
        
        elif "help" in user_message.lower():
            return "I'm here to help! What topic would you like to discuss? I can help with questions about finance, technology, general knowledge, or just have a friendly chat."
        
        else:
            # Generic response based on style and detail preferences
            if response_style == 'conversational':
                if detail_level == 'concise':
                    return f"That's an interesting question about '{user_message}'! I'd be happy to help. What specifically would you like to know?"
                elif detail_level == 'detailed':
                    return f"Great question! '{user_message}' is a fascinating topic. I'd love to dive deep into this with you. What aspect interests you most?"
                else:
                    return f"Thanks for asking about '{user_message}'! I'd be glad to help you understand this better. What would you like to know?"
            
            elif response_style == 'professional':
                if detail_level == 'concise':
                    return f"Regarding your question about '{user_message}', I can provide a focused response. What specific information are you seeking?"
                else:
                    return f"Your inquiry about '{user_message}' is well-timed. I'd be happy to provide comprehensive information. What aspects would you like me to cover?"
            
            else:
                return f"I appreciate your question about '{user_message}'. How can I best assist you with this topic?"
    
    def test_connection(self) -> bool:
        """Test OpenAI API connection"""
        if not self.client:
            return False
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            return True
        except Exception as e:
            print(f"❌ OpenAI connection test failed: {e}")
            return False 