#!/bin/bash

# HumAIne-Chatbot Container Runner
# This script builds and runs the HumAIne-chatbot container

set -e

echo "🚀 HumAIne-Chatbot Container Setup"
echo "=================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/virtual_personas data/user_sessions logs

# Build the Docker image
echo "🔨 Building Docker image..."
docker build -t humaine-chatbot:latest .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully"
else
    echo "❌ Failed to build Docker image"
    exit 1
fi

# Stop any existing container
echo "🛑 Stopping existing container..."
docker stop humaine-chatbot-backend 2>/dev/null || true
docker rm humaine-chatbot-backend 2>/dev/null || true

# Run the container
echo "🚀 Starting container..."
docker run -d \
    --name humaine-chatbot-backend \
    -p 8000:8000 \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/logs:/app/logs \
    -e HOST=0.0.0.0 \
    -e PORT=8000 \
    -e OPENAI_API_KEY=${OPENAI_API_KEY:-your_openai_api_key_here} \
    -e LOG_LEVEL=INFO \
    humaine-chatbot:latest

if [ $? -eq 0 ]; then
    echo "✅ Container started successfully"
    echo "📊 Container status:"
    docker ps --filter name=humaine-chatbot-backend --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    echo ""
    echo "⏳ Waiting for container to be ready..."
    sleep 15
    
    # Test the container
    echo "🧪 Testing container..."
    python3 test_container.py
    
    echo ""
    echo "🎉 Container setup complete!"
    echo ""
    echo "📋 Useful commands:"
    echo "   View logs: docker logs humaine-chatbot-backend"
    echo "   Stop container: docker stop humaine-chatbot-backend"
    echo "   Restart container: docker restart humaine-chatbot-backend"
    echo "   Remove container: docker rm humaine-chatbot-backend"
    echo ""
    echo "🌐 API available at: http://localhost:8000"
    echo "📚 API docs at: http://localhost:8000/docs"
    
else
    echo "❌ Failed to start container"
    exit 1
fi 