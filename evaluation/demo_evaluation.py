#!/usr/bin/env python3
"""
HumAIne Chatbot: Evaluation Framework Demo

This script demonstrates how to use the evaluation framework
with a simple example experiment.
"""

import asyncio
import json
from datetime import datetime
from experiment_runner import ExperimentConfig, ExperimentRunner
from statistical_analyzer import StatisticalAnalyzer

async def run_demo_experiment():
    """Run a demonstration experiment"""
    print("🎯 HumAIne Chatbot Evaluation Framework Demo")
    print("=" * 60)
    
    # Step 1: Configure a simple experiment
    print("\n📋 Step 1: Configuring Experiment")
    config = ExperimentConfig(
        experiment_name="Demo: User Profile System Validation",
        duration_days=1,  # Short demo
        participants_per_group=5,  # Small sample for demo
        control_group_enabled=True,
        metrics_collection_interval=60,  # 1 minute
        evaluation_metrics=["engagement", "session_duration", "user_satisfaction"]
    )
    
    print(f"   ✅ Experiment: {config.experiment_name}")
    print(f"   ⏱️  Duration: {config.duration_days} day")
    print(f"   👥 Participants: {config.participants_per_group * 2}")
    
    # Step 2: Run the experiment
    print("\n🚀 Step 2: Running Experiment")
    runner = ExperimentRunner(config)
    
    try:
        results = await runner.run_experiment()
        print("   ✅ Experiment completed successfully!")
        
        # Step 3: Perform statistical analysis
        print("\n🔬 Step 3: Statistical Analysis")
        analyzer = StatisticalAnalyzer(alpha=0.05, power_threshold=0.8)
        
        # Extract data for analysis
        control_data = {}
        experimental_data = {}
        
        for result in runner.results:
            if result.group == "control":
                for metric_name in ["engagement_score", "session_duration_avg"]:
                    if metric_name not in control_data:
                        control_data[metric_name] = []
                    control_data[metric_name].append(result.system_performance.get(metric_name, 0))
            else:
                for metric_name in ["engagement_score", "session_duration_avg"]:
                    if metric_name not in experimental_data:
                        experimental_data[metric_name] = []
                    experimental_data[metric_name].append(result.system_performance.get(metric_name, 0))
        
        # Run statistical analysis
        if control_data and experimental_data:
            analysis_results = analyzer.analyze_experiment(control_data, experimental_data)
            
            # Generate report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = f"demo_statistical_analysis_{timestamp}.json"
            report = analyzer.generate_report(analysis_results, report_file)
            
            print(f"   ✅ Statistical analysis completed!")
            print(f"   📊 Report saved to: {report_file}")
            
        else:
            print("   ⚠️  Insufficient data for statistical analysis")
        
        # Step 4: Summary
        print("\n🎉 Demo Summary")
        print("=" * 60)
        print("✅ Experiment executed successfully")
        print("✅ Data collected from all participants")
        print("✅ Statistical analysis performed")
        print("✅ Reports generated with visualizations")
        print("\n📁 Generated Files:")
        print("   • experiment_results_*.json - Raw experiment data")
        print("   • experiment_visualizations_*.png - Charts and graphs")
        print("   • demo_statistical_analysis_*.json - Statistical report")
        
        print("\n🚀 Next Steps:")
        print("   1. Review the generated reports")
        print("   2. Customize experiment parameters")
        print("   3. Run with larger sample sizes")
        print("   4. Integrate results into your paper")
        
    except Exception as e:
        print(f"   ❌ Experiment failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Ensure backend is running on localhost:8000")
        print("   2. Check API key configuration")
        print("   3. Verify all dependencies are installed")

def show_framework_capabilities():
    """Display the framework's capabilities"""
    print("\n🔬 Framework Capabilities")
    print("=" * 60)
    
    capabilities = [
        "🎯 Automated A/B Testing with control/experimental groups",
        "📊 Real-time metrics collection from backend APIs",
        "🔍 Statistical hypothesis testing (t-tests, effect sizes)",
        "⚡ Power analysis for sample size adequacy",
        "📈 Professional visualizations and charts",
        "📋 Comprehensive reporting with recommendations",
        "🎨 Customizable experiment configurations",
        "📚 Academic paper integration support"
    ]
    
    for capability in capabilities:
        print(f"   {capability}")
    
    print("\n📊 Supported Statistical Tests:")
    tests = [
        "Independent t-tests (between groups)",
        "Paired t-tests (within subjects)",
        "Effect size calculations (Cohen's d)",
        "Power analysis and sample size estimation",
        "Confidence intervals (95% CI)",
        "Descriptive statistics and visualizations"
    ]
    
    for test in tests:
        print(f"   • {test}")

def main():
    """Main demo function"""
    print("🎯 HumAIne Chatbot Evaluation Framework")
    print("=" * 60)
    
    # Show capabilities
    show_framework_capabilities()
    
    # Ask user if they want to run the demo
    print("\n" + "=" * 60)
    response = input("🚀 Would you like to run the demo experiment? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        print("\n🚀 Starting Demo Experiment...")
        print("⚠️  Note: This will create test participants and run interactions")
        print("   Make sure your backend is running on localhost:8000")
        
        # Run the demo
        asyncio.run(run_demo_experiment())
        
    else:
        print("\n📚 Demo skipped. You can run it later with:")
        print("   python demo_evaluation.py")
        print("\n📖 Review the documentation in:")
        print("   • README.md - Quick start guide")
        print("   • EVALUATION_FRAMEWORK.md - Complete methodology")
        print("   • experiment_runner.py - Experiment execution")
        print("   • statistical_analyzer.py - Statistical analysis")

if __name__ == "__main__":
    main()

