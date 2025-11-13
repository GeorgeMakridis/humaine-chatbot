#!/bin/bash

# HumAIne-Chatbot OpenAI Setup Script
# This script sets up the OpenAI API integration

set -e

echo "🚀 HumAIne-Chatbot OpenAI Setup"
echo "================================"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# HumAIne-chatbot Configuration

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# OpenAI Configuration
OPENAI_API_KEY=<your-api-key-here>

# Other configurations...
HUMANE_API_KEY=test-api-key-123
LOG_LEVEL=INFO
EOF
    echo "✅ .env file created with your OpenAI API key"
else
    echo "✅ .env file already exists"
fi

# Export environment variables
echo "🔑 Loading environment variables..."
export $(cat .env | grep -v '^#' | xargs)

# Test OpenAI integration
echo "🧪 Testing OpenAI integration..."
if python3 test_openai_integration.py; then
    echo "✅ OpenAI integration test passed!"
else
    echo "❌ OpenAI integration test failed!"
    exit 1
fi

# Test the API server
echo "🌐 Testing API server..."
if python3 -c "
import requests
import time
import sys

# Start server in background
import subprocess
import os
os.environ.update({'OPENAI_API_KEY': '<your-api-key-here>'})

server = subprocess.Popen(['python', 'main.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait for server to start
time.sleep(10)

try:
    response = requests.get('http://localhost:8000/health', timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f'✅ Health check passed: {data}')
        if data.get('openai', {}).get('status') == 'connected':
            print('✅ OpenAI API connected successfully!')
            sys.exit(0)
        else:
            print(f'❌ OpenAI API not connected: {data.get(\"openai\")}')
            sys.exit(1)
    else:
        print(f'❌ Health check failed: {response.status_code}')
        sys.exit(1)
except Exception as e:
    print(f'❌ Health check error: {e}')
    sys.exit(1)
finally:
    server.terminate()
    server.wait()
"; then
    echo "✅ API server test passed!"
else
    echo "❌ API server test failed!"
    exit 1
fi

echo ""
echo "🎉 OpenAI integration setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Start the server: python main.py"
echo "   2. Test the API: curl http://localhost:8000/health"
echo "   3. Or use Docker: docker-compose up -d"
echo ""
echo "🌐 API will be available at: http://localhost:8000"
echo "📚 API docs at: http://localhost:8000/docs"
echo "🔍 Health check at: http://localhost:8000/health"
