#!/usr/bin/env python3
"""
Virtual Personas Generator for HumAIne Chatbot Evaluation
Generates 50 diverse virtual personas with detailed backstories and characteristics.
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Any
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")
openai.api_key = api_key

class VirtualPersonaGenerator:
    """Generates diverse virtual personas for chatbot evaluation."""
    
    def __init__(self):
        self.demographics = {
            'age_groups': ['18-25', '26-35', '36-45', '46-55', '56-65', '65+'],
            'education_levels': [
                'High School', 'Some College', 'Bachelor\'s Degree', 
                'Master\'s Degree', 'PhD', 'Professional Certification'
            ],
            'occupation_categories': [
                'Technology', 'Healthcare', 'Education', 'Finance', 'Marketing',
                'Engineering', 'Creative Arts', 'Sales', 'Research', 'Management',
                'Legal', 'Consulting', 'Non-profit', 'Government', 'Entrepreneurship'
            ],
            'expertise_domains': [
                'Artificial Intelligence', 'Data Science', 'Healthcare', 'Finance',
                'Education', 'Marketing', 'Engineering', 'Creative Arts', 'Legal',
                'Research', 'Business Strategy', 'Technology', 'Human Resources'
            ],
            'communication_styles': [
                'Formal and Professional', 'Casual and Friendly', 'Technical and Detailed',
                'Conversational and Engaging', 'Direct and Concise', 'Storytelling and Narrative'
            ],
            'personality_traits': [
                'Analytical and Logical', 'Creative and Innovative', 'Empathetic and Caring',
                'Ambitious and Driven', 'Patient and Thoughtful', 'Energetic and Enthusiastic'
            ]
        }
    
    def generate_persona_backstory(self, persona_id: int) -> Dict[str, Any]:
        """Generate a detailed backstory for a virtual persona."""
        
        prompt = f"""
        Create a detailed virtual persona for chatbot evaluation. This persona should be realistic and diverse.
        
        Persona ID: {persona_id}
        
        Generate a persona with the following characteristics:
        
        Demographics:
        - Age: Choose from {', '.join(self.demographics['age_groups'])}
        - Education: Choose from {', '.join(self.demographics['education_levels'])}
        - Occupation: Choose from {', '.join(self.demographics['occupation_categories'])}
        - Location: A realistic city/country
        - Marital Status: Single, Married, Divorced, etc.
        
        Professional Background:
        - Current Role: Specific job title and company
        - Years of Experience: Realistic number
        - Key Skills: 3-5 relevant skills
        - Career Goals: What they want to achieve
        
        Personal Characteristics:
        - Communication Style: Choose from {', '.join(self.demographics['communication_styles'])}
        - Personality: Choose from {', '.join(self.demographics['personality_traits'])}
        - Interests: Hobbies and personal interests
        - Values: What matters to them
        
        Expertise Areas:
        - Primary Domain: Choose from {', '.join(self.demographics['expertise_domains'])}
        - Secondary Domain: Another area of knowledge
        - Learning Goals: What they want to learn about
        
        Communication Preferences:
        - Preferred Topics: What they like to discuss
        - Avoided Topics: What they prefer not to discuss
        - Response Style: How they prefer to receive information
        
        Current Task/Goal:
        - Primary Objective: What specific task or goal are they trying to accomplish right now?
        - Urgency Level: High, Medium, or Low priority
        - Success Criteria: How will they know they've achieved their goal?
        - Obstacles: What challenges are they facing in achieving this goal?
        
        Create a realistic, engaging backstory that explains their background, motivations, current situation, and the specific task they're working on.
        Make each persona unique and diverse in terms of age, background, expertise, communication style, and current objectives.
        
        Return the response as a JSON object with these exact keys:
        {{
            "persona_id": {persona_id},
            "demographics": {{}},
            "professional_background": {{}},
            "personal_characteristics": {{}},
            "expertise_areas": {{}},
            "communication_preferences": {{}},
            "current_task": {{
                "primary_objective": "What they're trying to accomplish",
                "urgency_level": "High/Medium/Low",
                "success_criteria": "How they measure success",
                "obstacles": "Challenges they face"
            }},
            "backstory": "A detailed narrative explaining their background, current situation, and the task they're working on"
        }}
        """
        
        try:
            # Use the legacy API approach to avoid client initialization issues
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert at creating diverse, realistic virtual personas for research purposes. Generate detailed, engaging backstories that are suitable for chatbot evaluation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=1000
            )
            
            # Extract and parse the response
            content = response.choices[0].message.content
            # Try to extract JSON from the response
            if '{' in content and '}' in content:
                start = content.find('{')
                end = content.rfind('}') + 1
                json_str = content[start:end]
                persona_data = json.loads(json_str)
                
                # Ensure all required fields are present
                required_fields = [
                    "persona_id", "demographics", "professional_background", 
                    "personal_characteristics", "expertise_areas", 
                    "communication_preferences", "backstory"
                ]
                
                for field in required_fields:
                    if field not in persona_data:
                        persona_data[field] = "Not specified"
                
                return persona_data
            else:
                # Fallback if JSON parsing fails
                return self._create_fallback_persona(persona_id)
                
        except Exception as e:
            print(f"Error generating persona {persona_id}: {e}")
            return self._create_fallback_persona(persona_id)
    
    def _create_fallback_persona(self, persona_id: int) -> Dict[str, Any]:
        """Create a fallback persona if API call fails."""
        return {
            "persona_id": persona_id,
            "demographics": {
                "age": random.choice(self.demographics['age_groups']),
                "education": random.choice(self.demographics['education_levels']),
                "occupation": random.choice(self.demographics['occupation_categories']),
                "location": "New York, USA",
                "marital_status": "Single"
            },
            "professional_background": {
                "current_role": "Software Engineer",
                "years_experience": random.randint(1, 15),
                "key_skills": ["Python", "Machine Learning", "Data Analysis"],
                "career_goals": "Become a senior data scientist"
            },
            "personal_characteristics": {
                "communication_style": random.choice(self.demographics['communication_styles']),
                "personality": random.choice(self.demographics['personality_traits']),
                "interests": ["Technology", "Reading", "Travel"],
                "values": ["Innovation", "Learning", "Collaboration"]
            },
            "expertise_areas": {
                "primary_domain": random.choice(self.demographics['expertise_domains']),
                "secondary_domain": random.choice(self.demographics['expertise_domains']),
                "learning_goals": "Advanced AI techniques"
            },
            "communication_preferences": {
                "preferred_topics": ["Technology", "Career Development", "Innovation"],
                "avoided_topics": ["Politics", "Personal Finance"],
                "response_style": "Clear and concise with examples"
            },
            "current_task": {
                "primary_objective": "Learn advanced machine learning techniques",
                "urgency_level": random.choice(["High", "Medium", "Low"]),
                "success_criteria": "Complete a machine learning project successfully",
                "obstacles": "Limited time and complex concepts"
            },
            "backstory": f"Persona {persona_id} is a fallback persona created due to API limitations."
        }
    
    def generate_all_personas(self, count: int = 50) -> List[Dict[str, Any]]:
        """Generate the specified number of virtual personas."""
        print(f"🎭 Generating {count} virtual personas...")
        
        personas = []
        for i in range(1, count + 1):
            print(f"Creating persona {i}/{count}...")
            persona = self.generate_persona_backstory(i)
            personas.append(persona)
            
            # Add a small delay to avoid rate limiting
            import time
            time.sleep(0.5)
        
        return personas
    
    def save_personas(self, personas: List[Dict[str, Any]], filename: str = None):
        """Save personas to a JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"virtual_personas_{timestamp}.json"
        
        filepath = filename
        
        with open(filepath, 'w') as f:
            json.dump({
                "metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "total_personas": len(personas),
                    "generator_version": "1.0"
                },
                "personas": personas
            }, f, indent=2)
        
        print(f"💾 Saved {len(personas)} personas to {filepath}")
        return filepath

def main():
    """Main function to generate virtual personas."""
    generator = VirtualPersonaGenerator()
    
    # Generate 50 personas
    personas = generator.generate_all_personas(50)
    
    # Save to file
    filename = generator.save_personas(personas)
    
    # Print summary
    print(f"\n🎉 Successfully generated {len(personas)} virtual personas!")
    print(f"📁 Saved to: {filename}")
    
    # Print a sample persona
    if personas:
        print(f"\n📋 Sample Persona Preview:")
        sample = personas[0]
        print(f"ID: {sample['persona_id']}")
        print(f"Age: {sample['demographics'].get('age', 'N/A')}")
        print(f"Occupation: {sample['professional_background'].get('current_role', 'N/A')}")
        print(f"Expertise: {sample['expertise_areas'].get('primary_domain', 'N/A')}")
        print(f"Communication Style: {sample['personal_characteristics'].get('communication_style', 'N/A')}")

if __name__ == "__main__":
    main()
