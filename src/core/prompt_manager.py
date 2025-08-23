"""
Prompt Manager for HumAIne-chatbot

This module manages prompt enrichment based on user profiles and personalization
parameters, enabling dynamic adaptation of chatbot responses.
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..models.schemas import UserProfile


class PromptManager:
    """Manages prompt enrichment and personalization"""
    
    def __init__(self):
        """Initialize the prompt manager"""
        self.prompt_templates = self._load_prompt_templates()
        self.personalization_rules = self._load_personalization_rules()
    
    def _load_prompt_templates(self) -> Dict[str, str]:
        """Load prompt templates for different scenarios"""
        return {
            "general": "You are a helpful AI assistant. {personalization_context}",
            "technical": "You are a technical AI assistant with expertise in various domains. {personalization_context}",
            "casual": "You are a friendly and conversational AI assistant. {personalization_context}",
            "professional": "You are a professional AI assistant focused on providing accurate and helpful information. {personalization_context}",
            "educational": "You are an educational AI assistant designed to help users learn and understand concepts. {personalization_context}"
        }
    
    def _load_personalization_rules(self) -> Dict[str, Dict[str, Any]]:
        """Load personalization rules for different user types"""
        return {
            "language_complexity": {
                "simple": {
                    "vocabulary_level": "basic",
                    "sentence_structure": "short",
                    "technical_depth": "minimal",
                    "explanation_style": "step_by_step"
                },
                "medium": {
                    "vocabulary_level": "standard",
                    "sentence_structure": "balanced",
                    "technical_depth": "moderate",
                    "explanation_style": "balanced"
                },
                "complex": {
                    "vocabulary_level": "advanced",
                    "sentence_structure": "detailed",
                    "technical_depth": "comprehensive",
                    "explanation_style": "comprehensive"
                }
            },
            "response_style": {
                "conversational": {
                    "tone": "friendly",
                    "formality": "casual",
                    "interaction_style": "engaging",
                    "use_emojis": True
                },
                "balanced": {
                    "tone": "neutral",
                    "formality": "moderate",
                    "interaction_style": "professional",
                    "use_emojis": False
                },
                "professional": {
                    "tone": "formal",
                    "formality": "high",
                    "interaction_style": "business_like",
                    "use_emojis": False
                },
                "enthusiastic": {
                    "tone": "excited",
                    "formality": "casual",
                    "interaction_style": "motivational",
                    "use_emojis": True
                }
            },
            "detail_level": {
                "concise": {
                    "response_length": "short",
                    "include_examples": False,
                    "include_context": "minimal",
                    "focus": "direct_answer"
                },
                "medium": {
                    "response_length": "moderate",
                    "include_examples": "when_helpful",
                    "include_context": "relevant",
                    "focus": "balanced"
                },
                "detailed": {
                    "response_length": "comprehensive",
                    "include_examples": True,
                    "include_context": "thorough",
                    "focus": "complete_explanation"
                }
            }
        }
    
    def enrich_prompt(self, base_prompt: str, user_id: str, 
                     personalization_params: Dict[str, Any]) -> str:
        """
        Enrich a base prompt with personalization context
        
        Args:
            base_prompt: The original user prompt
            user_id: User identifier
            personalization_params: Personalization parameters from user profiler
            
        Returns:
            Enriched prompt with personalization context
        """
        # Create personalization context
        personalization_context = self._create_personalization_context(personalization_params)
        
        # Select appropriate template
        template = self._select_template(personalization_params)
        
        # Create system prompt
        system_prompt = template.format(personalization_context=personalization_context)
        
        # Combine system prompt with user prompt
        enriched_prompt = f"{system_prompt}\n\nUser: {base_prompt}\n\nAssistant:"
        
        return enriched_prompt
    
    def _create_personalization_context(self, params: Dict[str, Any]) -> str:
        """Create personalization context string"""
        context_parts = []
        
        # Language complexity context
        complexity_rules = self.personalization_rules["language_complexity"].get(
            params.get("language_complexity", "medium"), {}
        )
        context_parts.append(f"Use {complexity_rules.get('vocabulary_level', 'standard')} vocabulary")
        context_parts.append(f"Provide {complexity_rules.get('explanation_style', 'balanced')} explanations")
        
        # Response style context
        style_rules = self.personalization_rules["response_style"].get(
            params.get("response_style", "balanced"), {}
        )
        context_parts.append(f"Maintain a {style_rules.get('tone', 'neutral')} tone")
        context_parts.append(f"Use {style_rules.get('formality', 'moderate')} language")
        
        # Detail level context
        detail_rules = self.personalization_rules["detail_level"].get(
            params.get("detail_level", "medium"), {}
        )
        context_parts.append(f"Provide {detail_rules.get('response_length', 'moderate')} responses")
        
        # User type specific context
        user_type = params.get("user_type", "general")
        if user_type == "technical":
            context_parts.append("Include technical details and specifications when relevant")
        elif user_type == "casual":
            context_parts.append("Keep responses friendly and approachable")
        elif user_type == "professional":
            context_parts.append("Focus on accuracy and professional presentation")
        
        # Engagement level context
        engagement_level = params.get("engagement_level", "medium")
        if engagement_level == "high":
            context_parts.append("Encourage continued interaction and ask follow-up questions")
        elif engagement_level == "low":
            context_parts.append("Provide direct, concise answers to maintain user interest")
        
        # Sentiment preference context
        sentiment_preference = params.get("sentiment_preference", "neutral")
        if sentiment_preference == "positive":
            context_parts.append("Maintain an encouraging and positive tone")
        elif sentiment_preference == "negative":
            context_parts.append("Be empathetic and supportive in responses")
        
        return ". ".join(context_parts) + "."
    
    def _select_template(self, params: Dict[str, Any]) -> str:
        """Select appropriate prompt template based on user type"""
        user_type = params.get("user_type", "general")
        
        if user_type == "technical":
            return self.prompt_templates["technical"]
        elif user_type == "casual":
            return self.prompt_templates["casual"]
        elif user_type == "professional":
            return self.prompt_templates["professional"]
        elif user_type == "educational":
            return self.prompt_templates["educational"]
        else:
            return self.prompt_templates["general"]
    
    def create_conversation_context(self, user_id: str, 
                                  personalization_params: Dict[str, Any],
                                  conversation_history: List[Dict[str, str]]) -> str:
        """Create conversation context for multi-turn conversations"""
        context_parts = []
        
        # Add personalization context
        personalization_context = self._create_personalization_context(personalization_params)
        context_parts.append(f"Context: {personalization_context}")
        
        # Add conversation history (last 5 turns)
        if conversation_history:
            recent_history = conversation_history[-5:]
            history_text = "\n".join([
                f"{turn['role']}: {turn['content']}" 
                for turn in recent_history
            ])
            context_parts.append(f"Recent conversation:\n{history_text}")
        
        return "\n\n".join(context_parts)
    
    def generate_response_guidelines(self, personalization_params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response guidelines based on personalization parameters"""
        guidelines = {}
        
        # Language complexity guidelines
        complexity = personalization_params.get("language_complexity", "medium")
        complexity_rules = self.personalization_rules["language_complexity"].get(complexity, {})
        guidelines["language"] = complexity_rules
        
        # Response style guidelines
        style = personalization_params.get("response_style", "balanced")
        style_rules = self.personalization_rules["response_style"].get(style, {})
        guidelines["style"] = style_rules
        
        # Detail level guidelines
        detail = personalization_params.get("detail_level", "medium")
        detail_rules = self.personalization_rules["detail_level"].get(detail, {})
        guidelines["detail"] = detail_rules
        
        # User type specific guidelines
        user_type = personalization_params.get("user_type", "general")
        guidelines["user_type"] = user_type
        
        return guidelines
    
    def adapt_prompt_for_domain(self, base_prompt: str, domain: str, 
                               personalization_params: Dict[str, Any]) -> str:
        """Adapt prompt for specific domains (finance, healthcare, education, etc.)"""
        domain_contexts = {
            "finance": "You are a financial advisor AI assistant. Provide accurate financial information and advice while considering the user's financial literacy level.",
            "healthcare": "You are a healthcare information AI assistant. Provide helpful health information while always recommending professional medical consultation for specific health concerns.",
            "education": "You are an educational AI assistant. Help users learn and understand concepts through clear explanations and examples.",
            "technology": "You are a technology expert AI assistant. Provide technical guidance and explanations suitable for the user's technical background.",
            "general": "You are a helpful AI assistant."
        }
        
        domain_context = domain_contexts.get(domain, domain_contexts["general"])
        personalization_context = self._create_personalization_context(personalization_params)
        
        return f"{domain_context} {personalization_context}\n\nUser: {base_prompt}\n\nAssistant:"
    
    def create_feedback_prompt(self, user_feedback: str, 
                             personalization_params: Dict[str, Any]) -> str:
        """Create a prompt for handling user feedback"""
        feedback_context = self._create_personalization_context(personalization_params)
        
        return f"""You are an AI assistant that adapts to user feedback. {feedback_context}

User feedback: {user_feedback}

Please acknowledge the feedback and adjust your response style accordingly. Assistant:"""
    
    def create_error_recovery_prompt(self, error_context: str,
                                   personalization_params: Dict[str, Any]) -> str:
        """Create a prompt for error recovery scenarios"""
        recovery_context = self._create_personalization_context(personalization_params)
        
        return f"""You are an AI assistant that handles errors gracefully. {recovery_context}

Error context: {error_context}

Please provide a helpful response that addresses the issue while maintaining the appropriate tone and style. Assistant:"""
    
    def get_prompt_analytics(self, original_prompt: str, enriched_prompt: str) -> Dict[str, Any]:
        """Analyze prompt enrichment for monitoring and improvement"""
        original_length = len(original_prompt)
        enriched_length = len(enriched_prompt)
        
        return {
            "original_length": original_length,
            "enriched_length": enriched_length,
            "enrichment_ratio": enriched_length / max(original_length, 1),
            "additional_context_length": enriched_length - original_length,
            "timestamp": datetime.utcnow().isoformat()
        } 