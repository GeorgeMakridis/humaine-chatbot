#!/bin/bash

echo "🚀 Testing HumAIne-chatbot with curl commands"
echo "=============================================="

# Test 1: Start conversation
echo "1️⃣ Starting conversation..."
START_RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d '{"user_id":"curl_test_user"}' http://localhost:8000/conversation/start)
SESSION_ID=$(echo $START_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['session_id'])")
echo "✅ Session started: $SESSION_ID"

# Test 2: Ask main question
echo -e "\n2️⃣ Asking main question..."
MAIN_QUESTION="What are the best AI models for natural language processing?"
echo "👤 Question: $MAIN_QUESTION"

MESSAGE_RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"session_id\":\"$SESSION_ID\",\"message\":\"$MAIN_QUESTION\",\"typing_start_time\":1640995200000,\"typing_end_time\":1640995210000}" http://localhost:8000/conversation/message)
echo "🤖 Bot response:"
echo "$MESSAGE_RESPONSE" | python3 -m json.tool

# Test 3: Answer expertise questions
EXPERTISE_ANSWERS=(
    "I'm an expert in this field"
    "I want comprehensive details"
    "I'm interested in practical applications"
)

for i in "${!EXPERTISE_ANSWERS[@]}"; do
    echo -e "\n3️⃣ Answering expertise question $((i+1))..."
    ANSWER="${EXPERTISE_ANSWERS[$i]}"
    echo "👤 Answer: $ANSWER"
    
    RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"session_id\":\"$SESSION_ID\",\"message\":\"$ANSWER\",\"typing_start_time\":1640995200000,\"typing_end_time\":1640995210000}" http://localhost:8000/conversation/message)
    echo "🤖 Bot response:"
    echo "$RESPONSE" | python3 -m json.tool
done

echo -e "\n✅ Test completed!"
echo "==============================================" 