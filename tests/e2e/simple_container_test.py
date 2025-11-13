"""
Simple Container Test for HumAIne-chatbot

This script tests the containerized HumAIne-chatbot system
without requiring external dependencies.
"""

import subprocess
import time
import json
import sys


def check_docker():
    """Check if Docker is available"""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker found: {result.stdout.strip()}")
            return True
        else:
            print("❌ Docker not found")
            return False
    except FileNotFoundError:
        print("❌ Docker not installed")
        return False


def build_image():
    """Build the Docker image"""
    print("🔨 Building Docker image...")
    try:
        result = subprocess.run(['docker', 'build', '-t', 'humaine-chatbot:latest', '.'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker image built successfully")
            return True
        else:
            print(f"❌ Failed to build image: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False


def run_container():
    """Run the container"""
    print("🚀 Starting container...")
    
    # Stop any existing container
    subprocess.run(['docker', 'stop', 'humaine-chatbot-backend'], 
                  capture_output=True, text=True)
    subprocess.run(['docker', 'rm', 'humaine-chatbot-backend'], 
                  capture_output=True, text=True)
    
    try:
        result = subprocess.run([
            'docker', 'run', '-d',
            '--name', 'humaine-chatbot-backend',
            '-p', '8000:8000',
            '-e', 'HOST=0.0.0.0',
            '-e', 'PORT=8000',
            '-e', 'OPENAI_API_KEY=test_key',
            'humaine-chatbot:latest'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            container_id = result.stdout.strip()
            print(f"✅ Container started: {container_id}")
            return True
        else:
            print(f"❌ Failed to start container: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Container error: {e}")
        return False


def check_container_status():
    """Check if container is running"""
    try:
        result = subprocess.run(['docker', 'ps', '--filter', 'name=humaine-chatbot-backend'], 
                              capture_output=True, text=True)
        if 'humaine-chatbot-backend' in result.stdout:
            print("✅ Container is running")
            return True
        else:
            print("❌ Container is not running")
            return False
    except Exception as e:
        print(f"❌ Status check error: {e}")
        return False


def test_health_endpoint():
    """Test the health endpoint using curl"""
    print("🧪 Testing health endpoint...")
    
    # Wait for container to be ready
    print("⏳ Waiting for container to be ready...")
    time.sleep(20)
    
    try:
        result = subprocess.run([
            'curl', '-f', 'http://localhost:8000/health'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Health endpoint responded")
            try:
                data = json.loads(result.stdout)
                print(f"   Status: {data.get('status', 'unknown')}")
                print(f"   Active conversations: {data.get('active_conversations', 0)}")
                return True
            except json.JSONDecodeError:
                print("   Response is not valid JSON")
                return False
        else:
            print(f"❌ Health endpoint failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Health endpoint timeout")
        return False
    except Exception as e:
        print(f"❌ Health test error: {e}")
        return False


def test_root_endpoint():
    """Test the root endpoint"""
    print("🧪 Testing root endpoint...")
    
    try:
        result = subprocess.run([
            'curl', '-f', 'http://localhost:8000/'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Root endpoint responded")
            try:
                data = json.loads(result.stdout)
                print(f"   Message: {data.get('message', 'unknown')}")
                print(f"   Version: {data.get('version', 'unknown')}")
                return True
            except json.JSONDecodeError:
                print("   Response is not valid JSON")
                return False
        else:
            print(f"❌ Root endpoint failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Root endpoint timeout")
        return False
    except Exception as e:
        print(f"❌ Root test error: {e}")
        return False


def test_conversation_start():
    """Test starting a conversation"""
    print("🧪 Testing conversation start...")
    
    start_data = {
        "user_id": "test_user_123",
        "initial_context": {"domain": "technology"}
    }
    
    try:
        result = subprocess.run([
            'curl', '-f', '-X', 'POST',
            '-H', 'Content-Type: application/json',
            '-d', json.dumps(start_data),
            'http://localhost:8000/conversation/start'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Conversation start endpoint responded")
            try:
                data = json.loads(result.stdout)
                session_id = data.get('session_id', 'unknown')
                print(f"   Session ID: {session_id}")
                return session_id
            except json.JSONDecodeError:
                print("   Response is not valid JSON")
                return None
        else:
            print(f"❌ Conversation start failed: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        print("❌ Conversation start timeout")
        return None
    except Exception as e:
        print(f"❌ Conversation start error: {e}")
        return None


def test_send_message(session_id):
    """Test sending a message"""
    print("🧪 Testing message sending...")
    
    message_data = {
        "session_id": session_id,
        "message": "Hello! Can you explain what AI is?",
        "typing_start_time": int(time.time() * 1000) - 2000,
        "typing_end_time": int(time.time() * 1000) - 1000,
        "bot_message_time": int(time.time() * 1000)
    }
    
    try:
        result = subprocess.run([
            'curl', '-f', '-X', 'POST',
            '-H', 'Content-Type: application/json',
            '-d', json.dumps(message_data),
            'http://localhost:8000/conversation/message'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Message endpoint responded")
            try:
                data = json.loads(result.stdout)
                response = data.get('response', 'No response')
                print(f"   Bot response: {response[:50]}...")
                return True
            except json.JSONDecodeError:
                print("   Response is not valid JSON")
                return False
        else:
            print(f"❌ Message sending failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Message sending timeout")
        return False
    except Exception as e:
        print(f"❌ Message sending error: {e}")
        return False


def get_container_logs():
    """Get container logs"""
    print("📋 Container logs:")
    try:
        result = subprocess.run(['docker', 'logs', 'humaine-chatbot-backend'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            logs = result.stdout.strip()
            if logs:
                print(logs[-500:])  # Last 500 characters
            else:
                print("   No logs available")
        else:
            print("   Could not retrieve logs")
    except Exception as e:
        print(f"   Log retrieval error: {e}")


def cleanup():
    """Clean up the container"""
    print("🧹 Cleaning up...")
    subprocess.run(['docker', 'stop', 'humaine-chatbot-backend'], 
                  capture_output=True, text=True)
    subprocess.run(['docker', 'rm', 'humaine-chatbot-backend'], 
                  capture_output=True, text=True)
    print("✅ Cleanup complete")


def main():
    """Main test function"""
    print("🚀 HumAIne-Chatbot Container Test")
    print("=" * 50)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is required for this test")
        sys.exit(1)
    
    # Build image
    if not build_image():
        print("❌ Failed to build image")
        sys.exit(1)
    
    # Run container
    if not run_container():
        print("❌ Failed to start container")
        sys.exit(1)
    
    # Wait a bit
    time.sleep(5)
    
    # Check container status
    if not check_container_status():
        print("❌ Container is not running")
        get_container_logs()
        cleanup()
        sys.exit(1)
    
    # Run tests
    tests = [
        ("Health Endpoint", test_health_endpoint),
        ("Root Endpoint", test_root_endpoint),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    # Test conversation flow
    print(f"\n{'='*20} Conversation Flow {'='*20}")
    session_id = test_conversation_start()
    if session_id:
        passed += 1
        print("✅ Conversation Start PASSED")
        
        if test_send_message(session_id):
            passed += 1
            print("✅ Message Sending PASSED")
        else:
            print("❌ Message Sending FAILED")
    else:
        print("❌ Conversation Start FAILED")
    
    total += 2  # Conversation start + message sending
    
    print(f"\n{'='*50}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The container is working correctly.")
        print("\n💡 The HumAIne-chatbot backend is running in the container.")
        print("🌐 API available at: http://localhost:8000")
        print("📚 API docs at: http://localhost:8000/docs")
    else:
        print("⚠️  Some tests failed. Check the container logs:")
        get_container_logs()
    
    # Ask if user wants to keep the container running
    print("\n🤔 Keep container running? (y/n): ", end="")
    try:
        response = input().lower().strip()
        if response not in ['y', 'yes']:
            cleanup()
            print("✅ Container stopped and removed")
        else:
            print("✅ Container kept running")
            print("📋 Commands:")
            print("   View logs: docker logs humaine-chatbot-backend")
            print("   Stop: docker stop humaine-chatbot-backend")
            print("   Remove: docker rm humaine-chatbot-backend")
    except KeyboardInterrupt:
        cleanup()
        print("\n✅ Container stopped and removed")


if __name__ == "__main__":
    main() 