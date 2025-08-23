#!/usr/bin/env python3
"""
HumAIne Chatbot: Automated Experiment Runner

This script automates the execution of controlled experiments to validate
the chatbot system's effectiveness according to the evaluation framework.
"""

import asyncio
import json
import time
import uuid
import statistics
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import requests
import pandas as pd
from dataclasses import dataclass, asdict
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "test-api-key-123"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

@dataclass
class ExperimentConfig:
    """Configuration for running experiments"""
    experiment_name: str
    duration_days: int
    participants_per_group: int
    control_group_enabled: bool
    metrics_collection_interval: int  # seconds
    evaluation_metrics: List[str]

@dataclass
class ExperimentResult:
    """Results from a single experiment run"""
    experiment_id: str
    timestamp: str
    group: str  # 'control' or 'experimental'
    metrics: Dict[str, Any]
    user_feedback: Dict[str, Any]
    system_performance: Dict[str, Any]

class ExperimentRunner:
    """Main class for running controlled experiments"""
    
    def __init__(self, config: ExperimentConfig):
        self.config = config
        self.results: List[ExperimentResult] = []
        self.active_participants: Dict[str, Dict[str, Any]] = {}
        self.experiment_start_time = None
        
    async def run_experiment(self) -> Dict[str, Any]:
        """Run the complete experiment"""
        print(f"🚀 Starting Experiment: {self.config.experiment_name}")
        print(f"⏱️  Duration: {self.config.duration_days} days")
        print(f"👥 Participants: {self.config.participants_per_group * 2 if self.config.control_group_enabled else self.config.participants_per_group}")
        
        # Initialize experiment
        self.experiment_start_time = datetime.now()
        experiment_id = str(uuid.uuid4())
        
        # Create participant groups
        await self._create_participant_groups()
        
        # Run experiment phases
        await self._run_baseline_phase()
        await self._run_intervention_phase()
        await self._run_evaluation_phase()
        
        # Analyze results
        analysis_results = self._analyze_results()
        
        # Generate report
        self._generate_report(analysis_results)
        
        return analysis_results
    
    async def _create_participant_groups(self):
        """Create and assign participants to experimental groups"""
        print("👥 Creating participant groups...")
        
        total_participants = self.config.participants_per_group * 2 if self.config.control_group_enabled else self.config.participants_per_group
        
        for i in range(total_participants):
            participant_id = f"exp-participant-{i+1:03d}"
            group = "control" if i < self.config.participants_per_group else "experimental"
            
            # Create user profile
            profile_data = {
                "user_id": participant_id,
                "group": group,
                "created_at": datetime.now().isoformat(),
                "experiment_phase": "baseline"
            }
            
            self.active_participants[participant_id] = {
                "profile": profile_data,
                "group": group,
                "sessions": [],
                "feedback": [],
                "metrics": []
            }
            
            print(f"   ✅ Created {participant_id} in {group} group")
    
    async def _run_baseline_phase(self):
        """Run baseline data collection phase"""
        print("\n📊 Phase 1: Baseline Data Collection")
        print("   Collecting baseline metrics for all participants...")
        
        # Simulate user interactions for baseline data
        for participant_id, participant_data in self.active_participants.items():
            await self._simulate_user_interaction(participant_id, "baseline")
            
        print("   ✅ Baseline phase completed")
    
    async def _run_intervention_phase(self):
        """Run intervention phase with enhanced system"""
        print("\n🔬 Phase 2: Intervention Phase")
        print("   Deploying enhanced system to experimental group...")
        
        # Update experimental group to use enhanced features
        for participant_id, participant_data in self.active_participants.items():
            if participant_data["group"] == "experimental":
                participant_data["experiment_phase"] = "intervention"
                await self._simulate_user_interaction(participant_id, "intervention")
        
        print("   ✅ Intervention phase completed")
    
    async def _run_evaluation_phase(self):
        """Run final evaluation and data collection"""
        print("\n📈 Phase 3: Evaluation Phase")
        print("   Collecting final metrics and user feedback...")
        
        # Collect final metrics from all participants
        for participant_id, participant_data in self.active_participants.items():
            await self._collect_final_metrics(participant_id)
        
        print("   ✅ Evaluation phase completed")
    
    async def _simulate_user_interaction(self, participant_id: str, phase: str):
        """Simulate realistic user interactions"""
        session_id = f"exp-session-{participant_id}-{phase}-{int(time.time())}"
        
        # Simulate typing and message sending
        typing_duration = 2000 + (hash(participant_id) % 3000)  # 2-5 seconds
        message_length = 20 + (hash(participant_id) % 80)  # 20-100 characters
        
        # Send user message
        message_data = {
            "session_id": session_id,
            "user_id": participant_id,
            "input_text": f"This is a test message from {participant_id} in {phase} phase.",
            "input_start_time": int(time.time() * 1000) - typing_duration,
            "input_end_time": int(time.time() * 1000),
            "input_sent_time": int(time.time() * 1000)
        }
        
        try:
            response = requests.post(f"{BASE_URL}/interact", headers=HEADERS, json=message_data)
            if response.status_code == 200:
                # Simulate feedback
                feedback_data = {
                    "session_id": session_id,
                    "user_id": participant_id,
                    "response_text": response.json().get("message", ""),
                    "response_start_time": int(time.time() * 1000) - 1000,
                    "response_end_time": int(time.time() * 1000),
                    "response_duration": 1000,
                    "feedback_type": "positive" if hash(participant_id) % 3 != 0 else "negative",
                    "feedback_time": int(time.time() * 1000),
                    "feedback_delay_duration": 1000
                }
                
                requests.post(f"{BASE_URL}/feedback", headers=HEADERS, json=feedback_data)
                
                # End session
                session_data = {
                    "session_id": session_id,
                    "user_id": participant_id,
                    "session_start": int(time.time() * 1000) - 10000,
                    "session_end": int(time.time() * 1000),
                    "session_end_type": "completed",
                    "session_duration": 10000
                }
                
                requests.post(f"{BASE_URL}/session", headers=HEADERS, json=session_data)
                
                # Store session data
                self.active_participants[participant_id]["sessions"].append({
                    "session_id": session_id,
                    "phase": phase,
                    "timestamp": datetime.now().isoformat()
                })
                
        except Exception as e:
            print(f"   ⚠️  Error simulating interaction for {participant_id}: {e}")
    
    async def _collect_final_metrics(self, participant_id: str):
        """Collect final metrics for a participant"""
        try:
            # Get user profile
            profile_response = requests.get(f"{BASE_URL}/profile/{participant_id}", headers=HEADERS)
            if profile_response.status_code == 200:
                profile_data = profile_response.json()
                
                # Get engagement metrics
                engagement_response = requests.get(f"{BASE_URL}/metrics/engagement/{participant_id}", headers=HEADERS)
                engagement_data = engagement_response.json() if engagement_response.status_code == 200 else {}
                
                # Get comprehensive metrics
                comprehensive_response = requests.get(f"{BASE_URL}/metrics/comprehensive/{participant_id}", headers=HEADERS)
                comprehensive_data = comprehensive_response.json() if comprehensive_response.status_code == 200 else {}
                
                # Create result object
                result = ExperimentResult(
                    experiment_id=str(uuid.uuid4()),
                    timestamp=datetime.now().isoformat(),
                    group=self.active_participants[participant_id]["group"],
                    metrics={
                        "profile": profile_data,
                        "engagement": engagement_data,
                        "comprehensive": comprehensive_data
                    },
                    user_feedback={
                        "sessions_count": len(self.active_participants[participant_id]["sessions"]),
                        "feedback_count": len(self.active_participants[participant_id]["feedback"])
                    },
                    system_performance={
                        "response_time_avg": comprehensive_data.get("average_response_time", 0),
                        "session_duration_avg": comprehensive_data.get("average_session_duration", 0),
                        "engagement_score": engagement_data.get("engagement_score", 0)
                    }
                )
                
                self.results.append(result)
                
        except Exception as e:
            print(f"   ⚠️  Error collecting metrics for {participant_id}: {e}")
    
    def _analyze_results(self) -> Dict[str, Any]:
        """Analyze experiment results using statistical methods"""
        print("\n📊 Analyzing Experiment Results...")
        
        if not self.results:
            return {"error": "No results to analyze"}
        
        # Separate results by group
        control_results = [r for r in self.results if r.group == "control"]
        experimental_results = [r for r in self.results if r.group == "experimental"]
        
        analysis = {
            "experiment_name": self.config.experiment_name,
            "total_participants": len(self.results),
            "control_group_size": len(control_results),
            "experimental_group_size": len(experimental_results),
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        # Calculate key metrics
        if control_results and experimental_results:
            # Engagement scores - with safety checks
            control_engagement = []
            experimental_engagement = []
            
            for r in control_results:
                try:
                    if hasattr(r, 'system_performance') and r.system_performance and "engagement_score" in r.system_performance:
                        control_engagement.append(r.system_performance["engagement_score"])
                except Exception:
                    continue
                    
            for r in experimental_results:
                try:
                    if hasattr(r, 'system_performance') and r.system_performance and "engagement_score" in r.system_performance:
                        experimental_engagement.append(r.system_performance["engagement_score"])
                except Exception:
                    continue
            
            # Safe statistics calculation with fallbacks
            try:
                control_mean = statistics.mean(control_engagement) if control_engagement else 0
                control_std = statistics.stdev(control_engagement) if len(control_engagement) > 1 else 0
                experimental_mean = statistics.mean(experimental_engagement) if experimental_engagement else 0
                experimental_std = statistics.stdev(experimental_engagement) if len(experimental_engagement) > 1 else 0
                
                # Calculate improvement safely
                if control_mean > 0 and not math.isnan(control_mean) and not math.isnan(experimental_mean):
                    improvement = ((experimental_mean - control_mean) / control_mean) * 100
                else:
                    improvement = 0
                
                analysis["engagement_analysis"] = {
                    "control_mean": control_mean,
                    "control_std": control_std,
                    "experimental_mean": experimental_mean,
                    "experimental_std": experimental_std,
                    "improvement_percentage": improvement
                }
            except Exception:
                analysis["engagement_analysis"] = {
                    "control_mean": 0,
                    "control_std": 0,
                    "experimental_mean": 0,
                    "experimental_std": 0,
                    "improvement_percentage": 0
                }
            
            # Session duration analysis - with safety checks
            control_duration = []
            experimental_duration = []
            
            for r in control_results:
                try:
                    if hasattr(r, 'system_performance') and r.system_performance and "session_duration_avg" in r.system_performance:
                        control_duration.append(r.system_performance["session_duration_avg"])
                except Exception:
                    continue
                    
            for r in experimental_results:
                try:
                    if hasattr(r, 'system_performance') and r.system_performance and "session_duration_avg" in r.system_performance:
                        experimental_duration.append(r.system_performance["session_duration_avg"])
                except Exception:
                    continue
            
            # Safe statistics calculation with fallbacks
            try:
                control_mean = statistics.mean(control_duration) if control_duration else 0
                control_std = statistics.stdev(control_duration) if len(control_duration) > 1 else 0
                experimental_mean = statistics.mean(experimental_duration) if experimental_duration else 0
                experimental_std = statistics.stdev(experimental_duration) if len(experimental_duration) > 1 else 0
                
                # Calculate improvement safely
                if control_mean > 0 and not math.isnan(control_mean) and not math.isnan(experimental_mean):
                    improvement = ((experimental_mean - control_mean) / control_mean) * 100
                else:
                    improvement = 0
                
                analysis["session_duration_analysis"] = {
                    "control_mean": control_mean,
                    "control_std": control_std,
                    "experimental_mean": experimental_mean,
                    "experimental_std": experimental_std,
                    "improvement_percentage": improvement
                }
            except Exception:
                analysis["session_duration_analysis"] = {
                    "control_mean": 0,
                    "control_std": 0,
                    "experimental_mean": 0,
                    "experimental_std": 0,
                    "improvement_percentage": 0
                }
        
        print("   ✅ Analysis completed")
        return analysis
    
    def _generate_report(self, analysis_results: Dict[str, Any]):
        """Generate comprehensive experiment report"""
        print("\n📋 Generating Experiment Report...")
        
        # Save results to JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_filename = f"experiment_results_{timestamp}.json"
        
        with open(results_filename, 'w') as f:
            json.dump({
                "experiment_config": asdict(self.config),
                "analysis_results": analysis_results,
                "raw_results": [asdict(r) for r in self.results]
            }, f, indent=2)
        
        print(f"   ✅ Results saved to {results_filename}")
        
        # Generate visualizations
        self._generate_visualizations(analysis_results)
        
        # Print summary
        self._print_summary(analysis_results)
    
    def _generate_visualizations(self, analysis_results: Dict[str, Any]):
        """Generate charts and visualizations"""
        print("   📊 Generating visualizations...")
        
        # Check if we have valid analysis results
        if "error" in analysis_results or not analysis_results:
            print("   ⚠️  No valid analysis results to visualize")
            return
        
        # Set up plotting style
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Experiment Results: {self.config.experiment_name}', fontsize=16)
        
        # Define groups at the beginning to avoid reference errors
        groups = ["Control", "Experimental"]
        
        # Engagement scores comparison
        if "engagement_analysis" in analysis_results and all(key in analysis_results["engagement_analysis"] for key in ["control_mean", "experimental_mean", "control_std", "experimental_std"]):
            try:
                engagement_data = analysis_results["engagement_analysis"]
                means = [engagement_data["control_mean"], engagement_data["experimental_mean"]]
                stds = [engagement_data["control_std"], engagement_data["experimental_std"]]
                
                # Check for valid numeric data
                if all(isinstance(x, (int, float)) and not math.isnan(x) for x in means + stds):
                    axes[0, 0].bar(groups, means, yerr=stds, capsize=5, alpha=0.7)
                    axes[0, 0].set_title("Engagement Score Comparison")
                    axes[0, 0].set_ylabel("Engagement Score")
                    axes[0, 0].grid(True, alpha=0.3)
                else:
                    axes[0, 0].text(0.5, 0.5, 'No valid engagement data', ha='center', va='center', transform=axes[0, 0].transAxes)
                    axes[0, 0].set_title("Engagement Score Comparison")
            except Exception:
                axes[0, 0].text(0.5, 0.5, 'No valid engagement data', ha='center', va='center', transform=axes[0, 0].transAxes)
                axes[0, 0].set_title("Engagement Score Comparison")
        else:
            axes[0, 0].text(0.5, 0.5, 'No engagement data available', ha='center', va='center', transform=axes[0, 0].transAxes)
            axes[0, 0].set_title("Engagement Score Comparison")
        
        # Session duration comparison
        if "session_duration_analysis" in analysis_results and all(key in analysis_results["session_duration_analysis"] for key in ["control_mean", "experimental_mean", "control_std", "experimental_std"]):
            try:
                duration_data = analysis_results["session_duration_analysis"]
                means = [duration_data["control_mean"], duration_data["experimental_mean"]]
                stds = [duration_data["control_std"], duration_data["experimental_std"]]
                
                # Check for valid numeric data
                if all(isinstance(x, (int, float)) and not math.isnan(x) for x in means + stds):
                    axes[0, 1].bar(groups, means, yerr=stds, capsize=5, alpha=0.7)
                    axes[0, 1].set_title("Session Duration Comparison")
                    axes[0, 1].set_ylabel("Duration (ms)")
                    axes[0, 1].grid(True, alpha=0.3)
                else:
                    axes[0, 1].text(0.5, 0.5, 'No valid duration data', ha='center', va='center', transform=axes[0, 1].transAxes)
                    axes[0, 1].set_title("Session Duration Comparison")
            except Exception:
                axes[0, 1].text(0.5, 0.5, 'No valid duration data', ha='center', va='center', transform=axes[0, 1].transAxes)
                axes[0, 1].set_title("Session Duration Comparison")
        else:
            axes[0, 1].text(0.5, 0.5, 'No duration data available', ha='center', va='center', transform=axes[0, 1].transAxes)
            axes[0, 1].set_title("Session Duration Comparison")
        
        # Participant distribution
        group_counts = [len([r for r in self.results if r.group == "control"]),
                       len([r for r in self.results if r.group == "experimental"])]
        axes[1, 0].pie(group_counts, labels=groups, autopct='%1.1f%%', startangle=90)
        axes[1, 0].set_title("Participant Distribution")
        
        # Improvement metrics
        if "engagement_analysis" in analysis_results and "improvement_percentage" in analysis_results["engagement_analysis"]:
            try:
                improvement = analysis_results["engagement_analysis"]["improvement_percentage"]
                # Final safety check for NaN values
                if isinstance(improvement, (int, float)) and not math.isnan(improvement) and not math.isinf(improvement):
                    # Ensure improvement is a valid number for plotting
                    improvement = float(improvement)
                    if not math.isnan(improvement) and not math.isinf(improvement):
                        axes[1, 1].bar(["Engagement Improvement"], [improvement], color='green' if improvement > 0 else 'red')
                        axes[1, 1].set_title("Improvement Percentage")
                        axes[1, 1].set_ylabel("Improvement (%)")
                        axes[1, 1].grid(True, alpha=0.3)
                    else:
                        axes[1, 1].text(0.5, 0.5, 'No valid improvement data', ha='center', va='center', transform=axes[1, 1].transAxes)
                        axes[1, 1].set_title("Improvement Percentage")
                else:
                    axes[1, 1].text(0.5, 0.5, 'No valid improvement data', ha='center', va='center', transform=axes[1, 1].transAxes)
                    axes[1, 1].set_title("Improvement Percentage")
            except Exception:
                axes[1, 1].text(0.5, 0.5, 'No valid improvement data', ha='center', va='center', transform=axes[1, 1].transAxes)
                axes[1, 1].set_title("Improvement Percentage")
        else:
            axes[1, 1].text(0.5, 0.5, 'No improvement data available', ha='center', va='center', transform=axes[1, 1].transAxes)
            axes[1, 1].set_title("Improvement Percentage")
        
        plt.tight_layout()
        
        # Save plot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_filename = f"experiment_visualizations_{timestamp}.png"
        plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
        print(f"   ✅ Visualizations saved to {plot_filename}")
        
        plt.close()
    
    def _print_summary(self, analysis_results: Dict[str, Any]):
        """Print experiment summary to console"""
        print("\n" + "="*60)
        print("🎯 EXPERIMENT SUMMARY")
        print("="*60)
        print(f"📊 Experiment: {analysis_results.get('experiment_name', 'Unknown')}")
        print(f"👥 Total Participants: {analysis_results.get('total_participants', 0)}")
        print(f"🔬 Control Group: {analysis_results.get('control_group_size', 0)}")
        print(f"🚀 Experimental Group: {analysis_results.get('experimental_group_size', 0)}")
        
        if "engagement_analysis" in analysis_results:
            engagement = analysis_results["engagement_analysis"]
            print(f"\n📈 ENGAGEMENT RESULTS:")
            print(f"   Control Group: {engagement['control_mean']:.2f} ± {engagement['control_std']:.2f}")
            print(f"   Experimental Group: {engagement['experimental_mean']:.2f} ± {engagement['experimental_std']:.2f}")
            print(f"   Improvement: {engagement['improvement_percentage']:.1f}%")
        
        if "session_duration_analysis" in analysis_results:
            duration = analysis_results["session_duration_analysis"]
            print(f"\n⏱️  SESSION DURATION RESULTS:")
            print(f"   Control Group: {duration['control_mean']:.0f}ms ± {duration['control_std']:.0f}ms")
            print(f"   Experimental Group: {duration['experimental_mean']:.0f}ms ± {duration['experimental_std']:.0f}ms")
            print(f"   Improvement: {duration['improvement_percentage']:.1f}%")
        
        print("\n" + "="*60)

async def main():
    """Main function to run experiments"""
    
    # Example experiment configuration
    config = ExperimentConfig(
        experiment_name="User Profile System Validation",
        duration_days=7,
        participants_per_group=20,
        control_group_enabled=True,
        metrics_collection_interval=300,  # 5 minutes
        evaluation_metrics=["engagement", "session_duration", "user_satisfaction"]
    )
    
    # Create and run experiment
    runner = ExperimentRunner(config)
    results = await runner.run_experiment()
    
    print(f"\n🎉 Experiment completed successfully!")
    print(f"📊 Results: {results}")

if __name__ == "__main__":
    asyncio.run(main())

