#!/usr/bin/env python3
"""
Simple launcher for HumAIne Chatbot Evaluation
Run this script to start the comprehensive evaluation process.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add evaluation directory to path
evaluation_dir = Path(__file__).parent
sys.path.insert(0, str(evaluation_dir))

def check_requirements():
    """Check if required packages are installed."""
    required_packages = [
        'openai', 'aiohttp', 'pandas', 'numpy', 
        'matplotlib', 'seaborn', 'requests', 'dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install them with:")
        print(f"   pip install -r {evaluation_dir}/evaluation_requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_backend():
    """Check if the HumAIne backend is running."""
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ HumAIne backend is running")
            return True
        else:
            print("⚠️  Backend responded but not healthy")
            return False
    except Exception as e:
        print("❌ HumAIne backend is not running")
        print("   Please start it first with: docker-compose up -d")
        return False

def check_environment():
    """Check if environment variables are set."""
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_key = os.getenv('OPENAI_API_KEY')
    if not openai_key:
        print("❌ OPENAI_API_KEY not found in environment")
        print("   Please set it in your .env file")
        return False
    
    print("✅ Environment variables are configured")
    return True

async def main():
    """Main evaluation launcher."""
    
    print("🚀 HumAIne Chatbot Evaluation Launcher")
    print("=" * 50)
    
    # Check prerequisites
    print("\n🔍 Checking prerequisites...")
    
    if not check_requirements():
        return
    
    if not check_backend():
        return
    
    if not check_environment():
        return
    
    print("\n✅ All prerequisites met!")
    
    # Import and run the comprehensive evaluator
    try:
        from comprehensive_evaluator import ComprehensiveEvaluator
        
        print("\n🚀 Starting comprehensive evaluation...")
        evaluator = ComprehensiveEvaluator()
        results = await evaluator.run_complete_evaluation()
        
        print(f"\n🎉 Evaluation completed successfully!")
        print(f"📊 Generated {len(results['personas'])} virtual personas")
        print(f"💬 Completed {len(results['conversations'])} conversation sessions")
        print(f"📝 Created {len(results['reports'])} analysis reports")
        print(f"🎨 Generated {len(results['visualizations'])} visualizations")
        print(f"\n📁 All results saved to: evaluation/results/")
        
        # Show summary of generated files
        print(f"\n📋 Generated Files:")
        for report_type, filepath in results['reports'].items():
            print(f"   📝 {report_type}: {Path(filepath).name}")
        
        for viz_type, filepath in results['visualizations'].items():
            print(f"   🎨 {viz_type}: {Path(filepath).name}")
        
        print(f"\n📊 Comprehensive Results: {Path(results['metadata']['evaluation_timestamp']).name}")
        
    except Exception as e:
        print(f"\n❌ Error during evaluation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Evaluation interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
