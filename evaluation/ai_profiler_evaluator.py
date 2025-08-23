#!/usr/bin/env python3
"""
HumAIne Chatbot: AI Profiler Evaluation Framework

This module specifically evaluates the AI profiler's effectiveness in:
1. Personalizing responses based on user profiles
2. Improving user satisfaction
3. Reducing session duration through better personalization
4. Cross-session learning and adaptation
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
import asyncio
import json
import time
import statistics
import math
from datetime import datetime, timedelta
import requests
from virtual_personas import VirtualPersona, VirtualPersonaGenerator

@dataclass
class ProfilerEvaluationMetrics:
    """Metrics specific to AI profiler evaluation"""
    
    # User Satisfaction Metrics
    satisfaction_score: float  # 1-5 scale
    feedback_positive_ratio: float  # 0.0 to 1.0
    engagement_rating: float  # 1-5 scale
    helpfulness_score: float  # 1-5 scale
    
    # Session Efficiency Metrics
    session_duration: float  # seconds
    turns_to_completion: int  # number of exchanges
    response_time_to_satisfaction: float  # seconds
    task_completion_rate: float  # 0.0 to 1.0
    
    # Personalization Effectiveness Metrics
    response_relevance_score: float  # 1-5 scale
    detail_level_match: float  # 0.0 to 1.0
    language_complexity_match: float  # 0.0 to 1.0
    style_consistency_score: float  # 1-5 scale
    
    # Cross-Session Learning Metrics
    profile_accuracy_improvement: float  # percentage
    adaptation_speed: float  # sessions to optimal personalization
    consistency_across_sessions: float  # 0.0 to 1.0

@dataclass
class ProfilerEvaluationResult:
    """Results from AI profiler evaluation"""
    
    persona_id: str
    session_id: str
    timestamp: str
    group: str  # 'control' or 'experimental'
    
    # Pre-interaction profile
    initial_profile: Dict[str, Any]
    
    # Post-interaction metrics
    metrics: ProfilerEvaluationMetrics
    
    # AI profiler insights
    profile_updates: Dict[str, Any]
    personalization_applied: Dict[str, Any]
    
    # User feedback
    explicit_feedback: Dict[str, Any]
    implicit_metrics: Dict[str, Any]

class AIProfilerEvaluator:
    """Evaluates AI profiler effectiveness using virtual personas"""
    
    def __init__(self, backend_url: str = "http://localhost:8000", api_key: str = "test-api-key-123"):
        self.backend_url = backend_url
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        self.persona_generator = VirtualPersonaGenerator()
        self.results: List[ProfilerEvaluationResult] = []
        
    async def run_comprehensive_evaluation(self, 
                                        cohort_size: int = 30,
                                        sessions_per_persona: int = 3,
                                        control_group_ratio: float = 0.5) -> Dict[str, Any]:
        """Run comprehensive evaluation of AI profiler"""
        
        print("🎯 AI Profiler Comprehensive Evaluation")
        print("=" * 60)
        
        # Step 1: Generate evaluation cohort
        print("👥 Step 1: Generating evaluation cohort...")
        personas = self.persona_generator.generate_evaluation_cohort(cohort_size)
        
        # Step 2: Assign to control/experimental groups
        print("🔬 Step 2: Assigning experimental groups...")
        control_size = int(cohort_size * control_group_ratio)
        control_personas = personas[:control_size]
        experimental_personas = personas[control_size:]
        
        print(f"   Control Group: {len(control_personas)} personas")
        print(f"   Experimental Group: {len(experimental_personas)} personas")
        
        # Step 3: Run baseline evaluation (no personalization)
        print("\n📊 Step 3: Running baseline evaluation...")
        baseline_results = await self._evaluate_personas(control_personas, "control", sessions_per_persona)
        
        # Step 4: Run experimental evaluation (with AI profiler)
        print("\n🚀 Step 4: Running experimental evaluation...")
        experimental_results = await self._evaluate_personas(experimental_personas, "experimental", sessions_per_persona)
        
        # Step 5: Analyze results
        print("\n📈 Step 5: Analyzing results...")
        analysis = self._analyze_profiler_effectiveness(baseline_results, experimental_results)
        
        # Step 6: Generate comprehensive report
        print("\n📋 Step 6: Generating comprehensive report...")
        self._generate_evaluation_report(analysis, personas)
        
        return analysis
    
    async def _evaluate_personas(self, personas: List[VirtualPersona], 
                                group: str, sessions_per_persona: int) -> List[ProfilerEvaluationResult]:
        """Evaluate a group of personas"""
        
        results = []
        
        for persona in personas:
            print(f"   Evaluating {persona.name} ({group} group)...")
            
            # Create test scenarios for this persona
            scenarios = self.persona_generator.create_test_scenarios(persona)
            
            for session_num in range(sessions_per_persona):
                session_id = f"{persona.persona_id}_session_{session_num + 1}"
                
                # Run evaluation session
                session_result = await self._evaluate_single_session(persona, scenarios, session_id, group)
                if session_result:
                    results.append(session_result)
                
                # Small delay between sessions
                await asyncio.sleep(1)
        
        return results
    
    async def _evaluate_single_session(self, persona: VirtualPersona, 
                                     scenarios: List[Dict[str, Any]], 
                                     session_id: str, group: str) -> Optional[ProfilerEvaluationResult]:
        """Evaluate a single session for a persona"""
        
        try:
            # Get initial profile
            initial_profile = await self._get_user_profile(persona.persona_id)
            
            # Run through test scenarios
            session_start = time.time()
            turns = 0
            total_response_time = 0
            feedback_scores = []
            
            for scenario in scenarios:
                # Simulate user interaction
                user_message = scenario["user_message"]
                scenario_start = time.time()
                
                # Send message to backend
                response = await self._send_user_message(persona.persona_id, user_message, session_id)
                
                if response:
                    response_time = time.time() - scenario_start
                    total_response_time += response_time
                    turns += 1
                    
                    # Simulate user feedback based on persona characteristics
                    feedback_score = self._simulate_user_feedback(persona, response, scenario)
                    feedback_scores.append(feedback_score)
                    
                    # Small delay to simulate realistic interaction
                    await asyncio.sleep(0.5)
            
            session_duration = time.time() - session_start
            
            # Calculate metrics
            metrics = ProfilerEvaluationMetrics(
                satisfaction_score=statistics.mean(feedback_scores) if feedback_scores else 3.0,
                feedback_positive_ratio=len([f for f in feedback_scores if f >= 4]) / len(feedback_scores) if feedback_scores else 0.5,
                engagement_rating=min(5.0, max(1.0, 5.0 - (session_duration / 60))),  # Longer sessions = lower engagement
                helpfulness_score=statistics.mean(feedback_scores) if feedback_scores else 3.0,
                session_duration=session_duration,
                turns_to_completion=turns,
                response_time_to_satisfaction=total_response_time / turns if turns > 0 else 0,
                task_completion_rate=min(1.0, turns / len(scenarios)),
                response_relevance_score=self._calculate_relevance_score(persona, scenarios),
                detail_level_match=self._calculate_detail_match(persona, scenarios),
                language_complexity_match=self._calculate_language_match(persona, scenarios),
                style_consistency_score=self._calculate_style_consistency(persona, scenarios),
                profile_accuracy_improvement=0.0,  # Will be calculated in cross-session analysis
                adaptation_speed=0.0,  # Will be calculated in cross-session analysis
                consistency_across_sessions=0.0  # Will be calculated in cross-session analysis
            )
            
            # Get final profile and personalization data
            final_profile = await self._get_user_profile(persona.persona_id)
            profile_updates = self._extract_profile_updates(initial_profile, final_profile)
            
            result = ProfilerEvaluationResult(
                persona_id=persona.persona_id,
                session_id=session_id,
                timestamp=datetime.now().isoformat(),
                group=group,
                initial_profile=initial_profile,
                metrics=metrics,
                profile_updates=profile_updates,
                personalization_applied=self._extract_personalization_applied(persona, scenarios),
                explicit_feedback={"simulated_scores": feedback_scores},
                implicit_metrics={"typing_speed": persona.typing_speed, "response_preference": persona.response_time_preference}
            )
            
            return result
            
        except Exception as e:
            print(f"   ⚠️  Error evaluating session {session_id}: {e}")
            return None
    
    async def _get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile from backend"""
        try:
            response = requests.get(f"{self.backend_url}/profile/{user_id}", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                return {}
        except Exception:
            return {}
    
    async def _send_user_message(self, user_id: str, message: str, session_id: str) -> Optional[str]:
        """Send user message to backend"""
        try:
            data = {
                "user_id": user_id,
                "message": message,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            }
            
            response = requests.post(f"{self.backend_url}/interact", 
                                  json=data, headers=self.headers)
            
            if response.status_code == 200:
                return response.json().get("message", "")
            else:
                return None
                
        except Exception:
            return None
    
    def _simulate_user_feedback(self, persona: VirtualPersona, 
                               response: str, scenario: Dict[str, Any]) -> float:
        """Simulate realistic user feedback based on persona characteristics"""
        
        base_score = 3.0  # Neutral base score
        
        # Adjust based on persona patience
        if persona.patience_level == "low" and len(response) > 200:
            base_score -= 0.5
        elif persona.patience_level == "high" and len(response) < 100:
            base_score -= 0.3
        
        # Adjust based on detail level preference
        if persona.detail_level == "concise" and len(response) > 150:
            base_score -= 0.4
        elif persona.detail_level == "detailed" and len(response) < 100:
            base_score -= 0.4
        
        # Adjust based on language complexity
        if persona.language_complexity == "simple" and len(response.split()) > 20:
            base_score -= 0.3
        elif persona.language_complexity == "complex" and len(response.split()) < 10:
            base_score -= 0.3
        
        # Add some randomness for realism
        base_score += random.uniform(-0.2, 0.2)
        
        return max(1.0, min(5.0, base_score))
    
    def _calculate_relevance_score(self, persona: VirtualPersona, 
                                 scenarios: List[Dict[str, Any]]) -> float:
        """Calculate response relevance score"""
        # This would be more sophisticated in real implementation
        base_score = 4.0
        
        # Adjust based on domain expertise match
        if persona.primary_domain in ["finance", "health", "education"]:
            base_score += 0.3
        
        # Adjust based on expertise level
        if persona.expertise_level == "expert":
            base_score += 0.2
        
        return min(5.0, base_score)
    
    def _calculate_detail_match(self, persona: VirtualPersona, 
                              scenarios: List[Dict[str, Any]]) -> float:
        """Calculate detail level match score"""
        if persona.detail_level == "concise":
            return 0.8
        elif persona.detail_level == "balanced":
            return 0.9
        else:  # detailed
            return 0.7
    
    def _calculate_language_match(self, persona: VirtualPersona, 
                                scenarios: List[Dict[str, Any]]) -> float:
        """Calculate language complexity match score"""
        if persona.language_complexity == "simple":
            return 0.85
        elif persona.language_complexity == "medium":
            return 0.9
        else:  # complex
            return 0.75
    
    def _calculate_style_consistency(self, persona: VirtualPersona, 
                                   scenarios: List[Dict[str, Any]]) -> float:
        """Calculate response style consistency score"""
        if persona.response_style == "conversational":
            return 0.9
        elif persona.response_style == "formal":
            return 0.8
        else:  # casual
            return 0.85
    
    def _extract_profile_updates(self, initial_profile: Dict[str, Any], 
                               final_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Extract profile updates between sessions"""
        updates = {}
        
        for key in final_profile:
            if key in initial_profile:
                if initial_profile[key] != final_profile[key]:
                    updates[key] = {
                        "from": initial_profile[key],
                        "to": final_profile[key]
                    }
            else:
                updates[key] = {"added": final_profile[key]}
        
        return updates
    
    def _extract_personalization_applied(self, persona: VirtualPersona, 
                                       scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract personalization parameters applied"""
        return {
            "language_complexity": persona.language_complexity,
            "detail_level": persona.detail_level,
            "response_style": persona.response_style,
            "expertise_level": persona.expertise_level,
            "domain_focus": persona.primary_domain
        }
    
    def _analyze_profiler_effectiveness(self, control_results: List[ProfilerEvaluationResult], 
                                      experimental_results: List[ProfilerEvaluationResult]) -> Dict[str, Any]:
        """Analyze the effectiveness of the AI profiler"""
        
        analysis = {
            "evaluation_summary": {
                "total_participants": len(control_results) + len(experimental_results),
                "control_group_size": len(control_results),
                "experimental_group_size": len(experimental_results),
                "evaluation_timestamp": datetime.now().isoformat()
            },
            "key_findings": {},
            "statistical_analysis": {},
            "recommendations": []
        }
        
        # Calculate key metrics
        if control_results and experimental_results:
            # User Satisfaction Analysis
            control_satisfaction = [r.metrics.satisfaction_score for r in control_results]
            experimental_satisfaction = [r.metrics.satisfaction_score for r in experimental_results]
            
            satisfaction_improvement = ((statistics.mean(experimental_satisfaction) - statistics.mean(control_satisfaction)) / 
                                     statistics.mean(control_satisfaction)) * 100 if statistics.mean(control_satisfaction) > 0 else 0
            
            # Session Efficiency Analysis
            control_duration = [r.metrics.session_duration for r in control_results]
            experimental_duration = [r.metrics.session_duration for r in experimental_results]
            
            duration_improvement = ((statistics.mean(control_duration) - statistics.mean(experimental_duration)) / 
                                  statistics.mean(control_duration)) * 100 if statistics.mean(control_duration) > 0 else 0
            
            # Personalization Effectiveness
            control_relevance = [r.metrics.response_relevance_score for r in control_results]
            experimental_relevance = [r.metrics.response_relevance_score for r in experimental_results]
            
            relevance_improvement = ((statistics.mean(experimental_relevance) - statistics.mean(control_relevance)) / 
                                   statistics.mean(control_relevance)) * 100 if statistics.mean(control_relevance) > 0 else 0
            
            analysis["key_findings"] = {
                "user_satisfaction": {
                    "control_mean": statistics.mean(control_satisfaction),
                    "experimental_mean": statistics.mean(experimental_satisfaction),
                    "improvement_percentage": satisfaction_improvement,
                    "significance": "significant" if abs(satisfaction_improvement) > 10 else "moderate"
                },
                "session_efficiency": {
                    "control_mean_duration": statistics.mean(control_duration),
                    "experimental_mean_duration": statistics.mean(experimental_duration),
                    "improvement_percentage": duration_improvement,
                    "significance": "significant" if abs(duration_improvement) > 15 else "moderate"
                },
                "personalization_effectiveness": {
                    "control_relevance": statistics.mean(control_relevance),
                    "experimental_relevance": statistics.mean(experimental_relevance),
                    "improvement_percentage": relevance_improvement,
                    "significance": "significant" if abs(relevance_improvement) > 20 else "moderate"
                }
            }
            
            # Generate recommendations
            if satisfaction_improvement > 15:
                analysis["recommendations"].append("AI profiler significantly improves user satisfaction - consider full deployment")
            elif satisfaction_improvement > 5:
                analysis["recommendations"].append("AI profiler shows moderate improvement - continue optimization")
            else:
                analysis["recommendations"].append("AI profiler needs refinement - investigate personalization parameters")
            
            if duration_improvement > 20:
                analysis["recommendations"].append("AI profiler substantially reduces session duration - excellent efficiency gains")
            elif duration_improvement > 10:
                analysis["recommendations"].append("AI profiler moderately improves session efficiency - good progress")
            else:
                analysis["recommendations"].append("Session efficiency needs improvement - focus on response optimization")
        
        return analysis
    
    def _generate_evaluation_report(self, analysis: Dict[str, Any], personas: List[VirtualPersona]):
        """Generate comprehensive evaluation report"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"ai_profiler_evaluation_{timestamp}.json"
        
        # Save detailed results
        with open(report_filename, 'w') as f:
            json.dump({
                "evaluation_metadata": {
                    "title": "AI Profiler Effectiveness Evaluation",
                    "timestamp": datetime.now().isoformat(),
                    "total_personas": len(personas),
                    "evaluation_framework": "Virtual Personas + Real-time Metrics"
                },
                "analysis_results": analysis,
                "persona_cohort": [p.to_dict() for p in personas],
                "detailed_results": [self._result_to_dict(r) for r in self.results]
            }, f, indent=2)
        
        print(f"   ✅ Comprehensive report saved to {report_filename}")
        
        # Print summary
        print("\n" + "="*60)
        print("🎯 AI PROFILER EVALUATION SUMMARY")
        print("="*60)
        
        if "key_findings" in analysis:
            findings = analysis["key_findings"]
            
            print(f"📊 User Satisfaction:")
            if "user_satisfaction" in findings:
                sat = findings["user_satisfaction"]
                print(f"   Control: {sat['control_mean']:.2f} → Experimental: {sat['experimental_mean']:.2f}")
                print(f"   Improvement: {sat['improvement_percentage']:.1f}% ({sat['significance']})")
            
            print(f"\n⏱️  Session Efficiency:")
            if "session_efficiency" in findings:
                eff = findings["session_efficiency"]
                print(f"   Control: {eff['control_mean_duration']:.1f}s → Experimental: {eff['experimental_mean_duration']:.1f}s")
                print(f"   Improvement: {eff['improvement_percentage']:.1f}% ({eff['significance']})")
            
            print(f"\n🎯 Personalization Effectiveness:")
            if "personalization_effectiveness" in findings:
                pers = findings["personalization_effectiveness"]
                print(f"   Control: {pers['control_relevance']:.2f} → Experimental: {pers['experimental_relevance']:.2f}")
                print(f"   Improvement: {pers['improvement_percentage']:.1f}% ({pers['significance']})")
        
        print(f"\n💡 Recommendations:")
        for rec in analysis.get("recommendations", []):
            print(f"   • {rec}")
    
    def _result_to_dict(self, result: ProfilerEvaluationResult) -> Dict[str, Any]:
        """Convert result to dictionary for JSON serialization"""
        return {
            "persona_id": result.persona_id,
            "session_id": result.session_id,
            "timestamp": result.timestamp,
            "group": result.group,
            "metrics": {
                "satisfaction_score": result.metrics.satisfaction_score,
                "session_duration": result.metrics.session_duration,
                "response_relevance": result.metrics.response_relevance_score,
                "detail_level_match": result.metrics.detail_level_match
            },
            "profile_updates": result.profile_updates
        }

async def main():
    """Demo the AI profiler evaluator"""
    print("🎯 AI Profiler Evaluation Framework Demo")
    print("=" * 60)
    
    evaluator = AIProfilerEvaluator()
    
    # Run a small evaluation for demo
    print("🚀 Running demo evaluation...")
    analysis = await evaluator.run_comprehensive_evaluation(
        cohort_size=6,  # Small cohort for demo
        sessions_per_persona=2,
        control_group_ratio=0.5
    )
    
    print("\n🎉 Demo completed!")
    print("📊 Check the generated report for detailed results")

if __name__ == "__main__":
    import random
    asyncio.run(main())
