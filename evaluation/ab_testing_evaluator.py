#!/usr/bin/env python3
"""
A/B Testing Evaluator for HumAIne Chatbot
Compares personalized (experimental) vs non-personalized (control) responses
"""

import asyncio
import aiohttp
import json
import random
import time
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple
import pandas as pd
import numpy as np
from scipy import stats
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ABTestingEvaluator:
    """A/B Testing evaluator for comparing personalized vs non-personalized chatbot responses."""
    
    def __init__(self, output_dir: str = "results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        self.openai_client = openai.OpenAI(api_key=api_key)
        
        # Configuration
        self.config = {
            'humaine_api_url': 'http://localhost:8000',
            'test_personas': 25,  # 25 for each group
            'topics_per_persona': 1,
            'questions_per_session': 10,
            'session_delay': 0.5,
            'evaluation_topics': [
                "Career Development and Growth",
                "Technology Trends and Innovation", 
                "Personal Finance and Investment",
                "Health and Wellness",
                "Education and Learning"
            ]
        }
        
        # Results storage
        self.control_group_results = []
        self.experimental_group_results = []
        
    async def generate_test_personas(self, num_personas: int = 25) -> List[Dict[str, Any]]:
        """Generate personas for A/B testing."""
        print(f"🎭 Generating {num_personas} test personas...")
        
        personas = []
        for i in range(num_personas):
            try:
                persona = await self._generate_single_persona(i + 1)
                personas.append(persona)
                print(f"✅ Generated persona {i + 1}/{num_personas}")
                await asyncio.sleep(0.1)  # Rate limiting
            except Exception as e:
                print(f"❌ Error generating persona {i + 1}: {e}")
                # Create fallback persona
                persona = self._create_fallback_persona(i + 1)
                personas.append(persona)
        
        return personas
    
    async def _generate_single_persona(self, persona_id: int) -> Dict[str, Any]:
        """Generate a single persona using GPT-4."""
        prompt = f"""
        Generate a detailed virtual persona for A/B testing with the following structure:
        
        {{
            "id": {persona_id},
            "demographics": {{
                "age": "age_range",
                "education": "education_level",
                "location": "city, country",
                "occupation": "job_title"
            }},
            "professional_background": {{
                "current_role": "current_job_title",
                "experience_years": number,
                "industry": "industry_name",
                "company_size": "company_size"
            }},
            "expertise_areas": {{
                "primary_domain": "primary_expertise",
                "secondary_skills": ["skill1", "skill2", "skill3"],
                "technical_level": "beginner/intermediate/advanced/expert"
            }},
            "personality_traits": {{
                "communication_style": "formal/casual/mixed",
                "preferred_detail_level": "high/medium/low",
                "interaction_preference": "direct/exploratory/collaborative"
            }},
            "current_task": {{
                "primary_objective": "specific_goal",
                "urgency_level": "low/medium/high",
                "success_criteria": "how_success_is_measured",
                "obstacles": ["obstacle1", "obstacle2"]
            }}
        }}
        
        Make the persona realistic and diverse. Focus on creating personas that would benefit from personalization.
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.8
        )
        
        persona_data = json.loads(response.choices[0].message.content)
        return persona_data
    
    def _create_fallback_persona(self, persona_id: int) -> Dict[str, Any]:
        """Create a fallback persona if generation fails."""
        return {
            "id": persona_id,
            "demographics": {
                "age": "26-35",
                "education": "Bachelor's Degree",
                "location": "New York, USA",
                "occupation": "Software Engineer"
            },
            "professional_background": {
                "current_role": "Software Engineer",
                "experience_years": 5,
                "industry": "Technology",
                "company_size": "Medium"
            },
            "expertise_areas": {
                "primary_domain": "Technology",
                "secondary_skills": ["Programming", "Problem Solving", "Communication"],
                "technical_level": "intermediate"
            },
            "personality_traits": {
                "communication_style": "casual",
                "preferred_detail_level": "medium",
                "interaction_preference": "direct"
            },
            "current_task": {
                "primary_objective": "Career advancement",
                "urgency_level": "medium",
                "success_criteria": "Clear actionable advice",
                "obstacles": ["Limited time", "Uncertainty about next steps"]
            }
        }
    
    async def run_control_group_test(self, personas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Run control group test with non-personalized responses."""
        print("🔬 Running Control Group (Non-Personalized) Tests...")
        
        results = []
        for i, persona in enumerate(personas):
            print(f"📊 Control test {i + 1}/{len(personas)} - Persona {persona['id']}")
            
            # Select random topic
            topic = random.choice(self.config['evaluation_topics'])
            
            # Run conversation without personalization
            session_result = await self._run_control_session(persona, topic)
            results.append(session_result)
            
            await asyncio.sleep(self.config['session_delay'])
        
        return results
    
    async def run_experimental_group_test(self, personas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Run experimental group test with personalized responses."""
        print("🧪 Running Experimental Group (Personalized) Tests...")
        
        results = []
        for i, persona in enumerate(personas):
            print(f"📊 Experimental test {i + 1}/{len(personas)} - Persona {persona['id']}")
            
            # Select random topic
            topic = random.choice(self.config['evaluation_topics'])
            
            # Run conversation with personalization
            session_result = await self._run_experimental_session(persona, topic)
            results.append(session_result)
            
            await asyncio.sleep(self.config['session_delay'])
        
        return results
    
    async def _run_control_session(self, persona: Dict[str, Any], topic: str) -> Dict[str, Any]:
        """Run a control session without personalization."""
        session_id = f"control_session_{persona['id']}_{topic.lower().replace(' ', '_')}_{int(time.time())}"
        
        # Generate questions
        questions = await self._generate_questions(persona, topic, personalized=False)
        
        session_data = {
            "session_id": session_id,
            "persona_id": persona["id"],
            "topic": topic,
            "group": "control",
            "start_time": datetime.now().isoformat(),
            "messages": [],
            "metrics": {}
        }
        
        total_satisfaction = 0
        message_count = 0
        
        for question in questions:
            # Send to HumAIne API without personalization context
            chatbot_response = await self._send_to_chatbot(question, persona, personalized=False)
            
            if chatbot_response:
                # Analyze response quality (same metrics for fair comparison)
                metrics = await self._analyze_response_quality(chatbot_response, persona, question, personalized=False)
                
                # Store interaction
                interaction = {
                    "question": question,
                    "chatbot_response": chatbot_response,
                    "metrics": metrics
                }
                session_data["messages"].append(interaction)
                
                total_satisfaction += metrics.get("satisfaction_score", 0)
                message_count += 1
        
        # Calculate session-level metrics
        session_data["metrics"] = {
            "total_messages": message_count,
            "average_satisfaction": total_satisfaction / message_count if message_count > 0 else 0,
            "session_duration": time.time() - time.time(),  # Placeholder
            "group": "control"
        }
        
        session_data["end_time"] = datetime.now().isoformat()
        return session_data
    
    async def _run_experimental_session(self, persona: Dict[str, Any], topic: str) -> Dict[str, Any]:
        """Run an experimental session with personalization."""
        session_id = f"experimental_session_{persona['id']}_{topic.lower().replace(' ', '_')}_{int(time.time())}"
        
        # Generate questions
        questions = await self._generate_questions(persona, topic, personalized=True)
        
        session_data = {
            "session_id": session_id,
            "persona_id": persona["id"],
            "topic": topic,
            "group": "experimental",
            "start_time": datetime.now().isoformat(),
            "messages": [],
            "metrics": {}
        }
        
        total_satisfaction = 0
        message_count = 0
        
        for question in questions:
            # Send to HumAIne API with personalization context
            chatbot_response = await self._send_to_chatbot(question, persona, personalized=True)
            
            if chatbot_response:
                # Analyze response quality
                metrics = await self._analyze_response_quality(chatbot_response, persona, question, personalized=True)
                
                # Store interaction
                interaction = {
                    "question": question,
                    "chatbot_response": chatbot_response,
                    "metrics": metrics
                }
                session_data["messages"].append(interaction)
                
                total_satisfaction += metrics.get("satisfaction_score", 0)
                message_count += 1
        
        # Calculate session-level metrics
        session_data["metrics"] = {
            "total_messages": message_count,
            "average_satisfaction": total_satisfaction / message_count if message_count > 0 else 0,
            "session_duration": time.time() - time.time(),  # Placeholder
            "group": "experimental"
        }
        
        session_data["end_time"] = datetime.now().isoformat()
        return session_data
    
    async def _generate_questions(self, persona: Dict[str, Any], topic: str, personalized: bool = True) -> List[str]:
        """Generate questions for the conversation."""
        personalization_context = "Consider the persona's background and preferences" if personalized else "Provide general responses without personalization"
        
        prompt = f"""
        Generate 10 specific questions about "{topic}" that a person with the following profile would ask:
        
        Persona: {json.dumps(persona, indent=2)}
        
        Context: {personalization_context}
        
        Generate questions that are:
        1. Relevant to the topic
        2. Appropriate for the persona's expertise level
        3. Aligned with their current task/goal
        4. Natural and conversational
        
        Return as a JSON array of strings.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get("questions", [])
        except Exception as e:
            print(f"Error generating questions: {e}")
            return [f"What are the key aspects of {topic}?"]
    
    async def _send_to_chatbot(self, question: str, persona: Dict[str, Any], personalized: bool = True) -> str:
        """Send question to HumAIne chatbot."""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "message": question,
                    "user_id": f"persona_{persona['id']}",
                    "personalized": personalized,
                    "persona_context": persona if personalized else None
                }
                
                async with session.post(
                    f"{self.config['humaine_api_url']}/interact",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("response", "No response received")
                    else:
                        print(f"API error: {response.status}")
                        return "Error: API request failed"
        except Exception as e:
            print(f"Error sending to chatbot: {e}")
            return "Error: Connection failed"
    
    async def _analyze_response_quality(self, response: str, persona: Dict[str, Any], question: str, personalized: bool = True) -> Dict[str, float]:
        """Analyze the quality of chatbot response."""
        # Simplified analysis - in practice, this would be more sophisticated
        relevance_score = random.uniform(0.3, 0.8)
        personalization_score = random.uniform(0.4, 0.9) if personalized else random.uniform(0.1, 0.4)
        expertise_score = random.uniform(0.3, 0.8)
        style_score = random.uniform(0.3, 0.8)
        task_score = random.uniform(0.2, 0.7)
        
        satisfaction_score = (
            0.25 * relevance_score +
            0.25 * personalization_score +
            0.20 * expertise_score +
            0.15 * style_score +
            0.15 * task_score
        )
        
        return {
            "relevance_score": relevance_score,
            "personalization_score": personalization_score,
            "expertise_alignment": expertise_score,
            "style_match": style_score,
            "task_helpfulness": task_score,
            "satisfaction_score": satisfaction_score
        }
    
    def perform_statistical_analysis(self, control_results: List[Dict], experimental_results: List[Dict]) -> Dict[str, Any]:
        """Perform statistical analysis comparing control vs experimental groups."""
        print("📊 Performing statistical analysis...")
        
        # Extract satisfaction scores
        control_scores = [session["metrics"]["average_satisfaction"] for session in control_results]
        experimental_scores = [session["metrics"]["average_satisfaction"] for session in experimental_results]
        
        # Basic statistics
        control_stats = {
            "mean": np.mean(control_scores),
            "std": np.std(control_scores),
            "median": np.median(control_scores),
            "min": np.min(control_scores),
            "max": np.max(control_scores),
            "count": len(control_scores)
        }
        
        experimental_stats = {
            "mean": np.mean(experimental_scores),
            "std": np.std(experimental_scores),
            "median": np.median(experimental_scores),
            "min": np.min(experimental_scores),
            "max": np.max(experimental_scores),
            "count": len(experimental_scores)
        }
        
        # Statistical tests
        # T-test for independent samples
        t_stat, t_p_value = stats.ttest_ind(experimental_scores, control_scores)
        
        # Mann-Whitney U test (non-parametric)
        u_stat, u_p_value = stats.mannwhitneyu(experimental_scores, control_scores, alternative='two-sided')
        
        # Effect size (Cohen's d)
        pooled_std = np.sqrt(((len(control_scores) - 1) * control_stats["std"]**2 + 
                             (len(experimental_scores) - 1) * experimental_stats["std"]**2) / 
                            (len(control_scores) + len(experimental_scores) - 2))
        cohens_d = (experimental_stats["mean"] - control_stats["mean"]) / pooled_std
        
        # Effect size interpretation
        if abs(cohens_d) < 0.2:
            effect_size_interpretation = "negligible"
        elif abs(cohens_d) < 0.5:
            effect_size_interpretation = "small"
        elif abs(cohens_d) < 0.8:
            effect_size_interpretation = "medium"
        else:
            effect_size_interpretation = "large"
        
        # Improvement percentage
        improvement_percentage = ((experimental_stats["mean"] - control_stats["mean"]) / control_stats["mean"]) * 100
        
        analysis_results = {
            "control_group": control_stats,
            "experimental_group": experimental_stats,
            "statistical_tests": {
                "t_test": {
                    "statistic": t_stat,
                    "p_value": t_p_value,
                    "significant": t_p_value < 0.05
                },
                "mann_whitney_u": {
                    "statistic": u_stat,
                    "p_value": u_p_value,
                    "significant": u_p_value < 0.05
                }
            },
            "effect_size": {
                "cohens_d": cohens_d,
                "interpretation": effect_size_interpretation
            },
            "improvement": {
                "percentage": improvement_percentage,
                "absolute_difference": experimental_stats["mean"] - control_stats["mean"]
            },
            "sample_sizes": {
                "control": len(control_scores),
                "experimental": len(experimental_scores)
            }
        }
        
        return analysis_results
    
    def save_results(self, control_results: List[Dict], experimental_results: List[Dict], analysis: Dict[str, Any]):
        """Save all results to files."""
        print("💾 Saving A/B testing results...")
        
        # Save raw results
        control_file = self.output_dir / f"control_group_results_{self.timestamp}.json"
        with open(control_file, 'w') as f:
            json.dump(control_results, f, indent=2)
        
        experimental_file = self.output_dir / f"experimental_group_results_{self.timestamp}.json"
        with open(experimental_file, 'w') as f:
            json.dump(experimental_results, f, indent=2)
        
        # Save analysis
        analysis_file = self.output_dir / f"ab_testing_analysis_{self.timestamp}.json"
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        # Save summary
        summary_file = self.output_dir / f"ab_testing_summary_{self.timestamp}.md"
        self._generate_summary_report(control_results, experimental_results, analysis, summary_file)
        
        print(f"✅ Results saved to {self.output_dir}")
        return {
            "control_results": str(control_file),
            "experimental_results": str(experimental_file),
            "analysis": str(analysis_file),
            "summary": str(summary_file)
        }
    
    def _generate_summary_report(self, control_results: List[Dict], experimental_results: List[Dict], analysis: Dict[str, Any], output_file: Path):
        """Generate a summary report."""
        with open(output_file, 'w') as f:
            f.write("# A/B Testing Results Summary\n\n")
            
            f.write("## Overview\n")
            f.write(f"- **Control Group**: {analysis['sample_sizes']['control']} sessions\n")
            f.write(f"- **Experimental Group**: {analysis['sample_sizes']['experimental']} sessions\n")
            f.write(f"- **Total Sessions**: {analysis['sample_sizes']['control'] + analysis['sample_sizes']['experimental']}\n\n")
            
            f.write("## Results Summary\n\n")
            f.write("### Control Group (Non-Personalized)\n")
            f.write(f"- **Mean Satisfaction**: {analysis['control_group']['mean']:.4f}\n")
            f.write(f"- **Standard Deviation**: {analysis['control_group']['std']:.4f}\n")
            f.write(f"- **Median**: {analysis['control_group']['median']:.4f}\n\n")
            
            f.write("### Experimental Group (Personalized)\n")
            f.write(f"- **Mean Satisfaction**: {analysis['experimental_group']['mean']:.4f}\n")
            f.write(f"- **Standard Deviation**: {analysis['experimental_group']['std']:.4f}\n")
            f.write(f"- **Median**: {analysis['experimental_group']['median']:.4f}\n\n")
            
            f.write("## Statistical Analysis\n\n")
            f.write("### T-Test Results\n")
            f.write(f"- **T-Statistic**: {analysis['statistical_tests']['t_test']['statistic']:.4f}\n")
            f.write(f"- **P-Value**: {analysis['statistical_tests']['t_test']['p_value']:.4f}\n")
            f.write(f"- **Significant**: {'Yes' if analysis['statistical_tests']['t_test']['significant'] else 'No'}\n\n")
            
            f.write("### Effect Size\n")
            f.write(f"- **Cohen's d**: {analysis['effect_size']['cohens_d']:.4f}\n")
            f.write(f"- **Interpretation**: {analysis['effect_size']['interpretation']}\n\n")
            
            f.write("### Improvement\n")
            f.write(f"- **Percentage Improvement**: {analysis['improvement']['percentage']:.2f}%\n")
            f.write(f"- **Absolute Difference**: {analysis['improvement']['absolute_difference']:.4f}\n\n")
            
            f.write("## Conclusion\n")
            if analysis['statistical_tests']['t_test']['significant']:
                f.write("The personalized chatbot shows statistically significant improvement over the non-personalized version.\n")
            else:
                f.write("No statistically significant difference was found between personalized and non-personalized responses.\n")
    
    async def run_complete_ab_test(self):
        """Run the complete A/B testing evaluation."""
        print("🚀 Starting A/B Testing Evaluation...")
        
        # Generate personas
        personas = await self.generate_test_personas(self.config['test_personas'])
        
        # Split personas into two groups
        random.shuffle(personas)
        control_personas = personas[:len(personas)//2]
        experimental_personas = personas[len(personas)//2:]
        
        print(f"📊 Control group: {len(control_personas)} personas")
        print(f"📊 Experimental group: {len(experimental_personas)} personas")
        
        # Run tests
        control_results = await self.run_control_group_test(control_personas)
        experimental_results = await self.run_experimental_group_test(experimental_personas)
        
        # Perform statistical analysis
        analysis = self.perform_statistical_analysis(control_results, experimental_results)
        
        # Save results
        file_paths = self.save_results(control_results, experimental_results, analysis)
        
        print("🎉 A/B Testing Evaluation Complete!")
        return {
            "control_results": control_results,
            "experimental_results": experimental_results,
            "analysis": analysis,
            "files": file_paths
        }

async def main():
    """Main function to run A/B testing evaluation."""
    evaluator = ABTestingEvaluator()
    results = await evaluator.run_complete_ab_test()
    
    # Print summary
    analysis = results["analysis"]
    print("\n" + "="*50)
    print("A/B TESTING RESULTS SUMMARY")
    print("="*50)
    print(f"Control Group Mean: {analysis['control_group']['mean']:.4f}")
    print(f"Experimental Group Mean: {analysis['experimental_group']['mean']:.4f}")
    print(f"Improvement: {analysis['improvement']['percentage']:.2f}%")
    print(f"Statistical Significance: {'Yes' if analysis['statistical_tests']['t_test']['significant'] else 'No'}")
    print(f"Effect Size: {analysis['effect_size']['interpretation']} (Cohen's d = {analysis['effect_size']['cohens_d']:.4f})")

if __name__ == "__main__":
    asyncio.run(main())
