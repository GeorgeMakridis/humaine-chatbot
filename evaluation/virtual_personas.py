#!/usr/bin/env python3
"""
HumAIne Chatbot: Virtual Personas for Evaluation

This module creates synthetic user personas with different characteristics
to systematically test the AI profiler's personalization capabilities.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import random
import json
from datetime import datetime

@dataclass
class VirtualPersona:
    """A synthetic user persona for systematic evaluation"""
    
    # Basic identity
    persona_id: str
    name: str
    age_group: str  # "young", "adult", "senior"
    
    # Communication preferences
    language_complexity: str  # "simple", "medium", "complex"
    detail_level: str  # "concise", "balanced", "detailed"
    response_style: str  # "formal", "conversational", "casual"
    
    # Domain expertise
    expertise_level: str  # "beginner", "intermediate", "expert"
    primary_domain: str  # "finance", "health", "education", "general"
    
    # Behavioral patterns
    patience_level: str  # "low", "medium", "high"
    engagement_style: str  # "passive", "active", "collaborative"
    
    # Session preferences
    preferred_session_length: str  # "short", "medium", "long"
    multitasking_tendency: str  # "low", "medium", "high"
    
    # Language characteristics
    typing_speed: float  # words per minute
    response_time_preference: float  # seconds
    grammar_accuracy: float  # 0.0 to 1.0
    
    # Emotional profile
    stress_level: str  # "low", "medium", "high"
    confidence_level: str  # "low", "medium", "high"
    
    # Evaluation scenarios
    test_scenarios: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert persona to dictionary for API calls"""
        return {
            "user_id": self.persona_id,
            "name": self.name,
            "age_group": self.age_group,
            "language_complexity": self.language_complexity,
            "detail_level": self.detail_level,
            "response_style": self.response_style,
            "expertise_level": self.expertise_level,
            "primary_domain": self.primary_domain,
            "patience_level": self.patience_level,
            "engagement_style": self.engagement_style,
            "preferred_session_length": self.preferred_session_length,
            "multitasking_tendency": self.multitasking_tendency,
            "typing_speed": self.typing_speed,
            "response_time_preference": self.response_time_preference,
            "grammar_accuracy": self.grammar_accuracy,
            "stress_level": self.stress_level,
            "confidence_level": self.confidence_level
        }

class VirtualPersonaGenerator:
    """Generates diverse virtual personas for evaluation"""
    
    def __init__(self):
        self.personas = []
        self._load_persona_templates()
    
    def _load_persona_templates(self):
        """Load predefined persona templates"""
        self.templates = {
            "young_beginner": {
                "age_group": "young",
                "expertise_level": "beginner",
                "language_complexity": "simple",
                "detail_level": "concise",
                "response_style": "casual",
                "patience_level": "low",
                "engagement_style": "active",
                "preferred_session_length": "short",
                "multitasking_tendency": "high",
                "typing_speed": 45.0,
                "response_time_preference": 2.0,
                "grammar_accuracy": 0.7,
                "stress_level": "medium",
                "confidence_level": "low"
            },
            "adult_intermediate": {
                "age_group": "adult",
                "expertise_level": "intermediate",
                "language_complexity": "medium",
                "detail_level": "balanced",
                "response_style": "conversational",
                "patience_level": "medium",
                "engagement_style": "collaborative",
                "preferred_session_length": "medium",
                "multitasking_tendency": "medium",
                "typing_speed": 35.0,
                "response_time_preference": 5.0,
                "grammar_accuracy": 0.9,
                "stress_level": "medium",
                "confidence_level": "medium"
            },
            "senior_expert": {
                "age_group": "senior",
                "expertise_level": "expert",
                "language_complexity": "complex",
                "detail_level": "detailed",
                "response_style": "formal",
                "patience_level": "high",
                "engagement_style": "passive",
                "preferred_session_length": "long",
                "multitasking_tendency": "low",
                "typing_speed": 25.0,
                "response_time_preference": 8.0,
                "grammar_accuracy": 0.95,
                "stress_level": "low",
                "confidence_level": "high"
            }
        }
    
    def generate_persona(self, template_name: str, persona_id: str, name: str, 
                        primary_domain: str = "general") -> VirtualPersona:
        """Generate a persona based on a template"""
        
        if template_name not in self.templates:
            raise ValueError(f"Unknown template: {template_name}")
        
        template = self.templates[template_name].copy()
        template.update({
            "persona_id": persona_id,
            "name": name,
            "primary_domain": primary_domain
        })
        
        # Add some randomization to make personas unique
        template["typing_speed"] += random.uniform(-5, 5)
        template["response_time_preference"] += random.uniform(-1, 1)
        template["grammar_accuracy"] = max(0.5, min(1.0, template["grammar_accuracy"] + random.uniform(-0.1, 0.1)))
        
        return VirtualPersona(**template)
    
    def generate_evaluation_cohort(self, size: int = 30) -> List[VirtualPersona]:
        """Generate a diverse cohort of personas for evaluation"""
        
        personas = []
        templates = list(self.templates.keys())
        domains = ["finance", "health", "education", "general", "technology"]
        
        for i in range(size):
            template = random.choice(templates)
            domain = random.choice(domains)
            persona_id = f"eval-persona-{i+1:03d}"
            name = f"Persona_{i+1}"
            
            persona = self.generate_persona(template, persona_id, name, domain)
            personas.append(persona)
        
        self.personas = personas
        return personas
    
    def create_test_scenarios(self, persona: VirtualPersona) -> List[Dict[str, Any]]:
        """Create realistic test scenarios for a persona"""
        
        scenarios = []
        
        # Scenario 1: Information seeking
        scenarios.append({
            "scenario_id": f"{persona.persona_id}_info_seek",
            "type": "information_seeking",
            "user_message": self._generate_info_seek_message(persona),
            "expected_outcome": "satisfactory_information",
            "success_criteria": ["relevant_response", "appropriate_detail_level", "helpful_format"]
        })
        
        # Scenario 2: Problem solving
        scenarios.append({
            "scenario_id": f"{persona.persona_id}_problem_solve",
            "type": "problem_solving",
            "user_message": self._generate_problem_message(persona),
            "expected_outcome": "problem_resolution",
            "success_criteria": ["clear_solution", "step_by_step_guidance", "confidence_building"]
        })
        
        # Scenario 3: Learning/exploration
        scenarios.append({
            "scenario_id": f"{persona.persona_id}_learning",
            "type": "learning_exploration",
            "user_message": self._generate_learning_message(persona),
            "expected_outcome": "knowledge_gain",
            "success_criteria": ["educational_value", "engagement", "retention"]
        })
        
        persona.test_scenarios = scenarios
        return scenarios
    
    def _generate_info_seek_message(self, persona: VirtualPersona) -> str:
        """Generate information-seeking message based on persona characteristics"""
        
        if persona.primary_domain == "finance":
            if persona.expertise_level == "beginner":
                return "What is a good way to start saving money?"
            elif persona.expertise_level == "intermediate":
                return "How should I diversify my investment portfolio?"
            else:
                return "What are the tax implications of different retirement account strategies?"
        
        elif persona.primary_domain == "health":
            if persona.expertise_level == "beginner":
                return "How can I improve my daily exercise routine?"
            elif persona.expertise_level == "intermediate":
                return "What should I consider when choosing health insurance?"
            else:
                return "How do I interpret advanced blood test results?"
        
        else:  # general
            if persona.expertise_level == "beginner":
                return "Can you help me understand this topic?"
            elif persona.expertise_level == "intermediate":
                return "I need some guidance on this subject."
            else:
                return "I'm looking for detailed analysis on this matter."
    
    def _generate_problem_message(self, persona: VirtualPersona) -> str:
        """Generate problem-solving message based on persona characteristics"""
        
        if persona.primary_domain == "finance":
            return "I'm having trouble managing my monthly budget. What should I do?"
        elif persona.primary_domain == "health":
            return "I'm struggling to maintain a healthy diet. Can you help?"
        else:
            return "I'm facing a challenge and need some advice."
    
    def _generate_learning_message(self, persona: VirtualPersona) -> str:
        """Generate learning/exploration message based on persona characteristics"""
        
        if persona.primary_domain == "finance":
            return "I want to learn more about investing. Where should I start?"
        elif persona.primary_domain == "health":
            return "I'm interested in learning about nutrition. What's important to know?"
        else:
            return "I'd like to explore this topic further. What should I focus on?"
    
    def save_personas(self, filename: str = None):
        """Save personas to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"virtual_personas_{timestamp}.json"
        
        data = {
            "generated_at": datetime.now().isoformat(),
            "total_personas": len(self.personas),
            "personas": [persona.to_dict() for persona in self.personas]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Saved {len(self.personas)} personas to {filename}")
        return filename
    
    def load_personas(self, filename: str) -> List[VirtualPersona]:
        """Load personas from JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        personas = []
        for persona_data in data["personas"]:
            # Reconstruct persona object
            persona = VirtualPersona(**persona_data)
            personas.append(persona)
        
        self.personas = personas
        print(f"✅ Loaded {len(personas)} personas from {filename}")
        return personas

def main():
    """Demo the virtual persona generator"""
    print("🎭 Virtual Persona Generator for HumAIne Evaluation")
    print("=" * 60)
    
    generator = VirtualPersonaGenerator()
    
    # Generate a small cohort for demo
    personas = generator.generate_evaluation_cohort(size=6)
    
    print(f"\n🎯 Generated {len(personas)} evaluation personas:")
    for persona in personas:
        print(f"   • {persona.name} ({persona.age_group}, {persona.expertise_level}, {persona.primary_domain})")
        print(f"     Language: {persona.language_complexity}, Detail: {persona.detail_level}")
        print(f"     Style: {persona.response_style}, Patience: {persona.patience_level}")
    
    # Create test scenarios for first persona
    print(f"\n🧪 Creating test scenarios for {personas[0].name}:")
    scenarios = generator.create_test_scenarios(personas[0])
    for scenario in scenarios:
        print(f"   • {scenario['type']}: {scenario['user_message']}")
    
    # Save personas
    filename = generator.save_personas()
    
    print(f"\n🚀 Next steps:")
    print(f"   1. Use these personas in your evaluation framework")
    print(f"   2. Run A/B tests with personalized vs. non-personalized responses")
    print(f"   3. Measure satisfaction, efficiency, and personalization effectiveness")
    print(f"   4. Analyze results for your research paper")

if __name__ == "__main__":
    main()
