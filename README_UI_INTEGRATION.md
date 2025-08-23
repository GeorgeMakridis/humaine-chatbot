# HumAIne UI Integration Guide

This guide explains how to use the HumAIne chatbot UI with the backend API.

## 🏗️ Architecture

The system consists of:
- **Frontend**: Stencil.js web component (`humaine-chatbot`)
- **Backend**: FastAPI server with RL agent integration
- **Data Flow**: UI sends exact JSON schemas → Backend processes with RL → Returns responses

## 🚀 Quick Start

### 1. Start the Backend

```bash
# Set your API key as environment variable
export HUMANE_API_KEY="your-secret-api-key"

# Start the backend
python main.py
```

The backend will run on `http://localhost:8000`

### 2. Start the UI

```bash
cd ui
npm start
```

The UI will run on `http://localhost:3335`

### 3. Test the Integration

Open `http://localhost:3335` in your browser. You should see:
- Configuration section for backend URL and API key
- Chatbot component below

## 🔑 Configuration

### Backend API Key

The backend reads the API key from the `HUMANE_API_KEY` environment variable:

```bash
export HUMANE_API_KEY="your-secret-api-key"
```

If no environment variable is set, it defaults to `"test-api-key-123"` for testing.

### UI Configuration

In the UI, you can configure:
- **Backend URL**: Where your FastAPI server is running (default: `http://localhost:8000`)
- **API Key**: Your secret API key for authentication

## 📡 API Endpoints

The backend implements these endpoints that match the UI's exact JSON schemas:

### POST `/interact`
Handles user messages. Expects data matching `UserPrompt.toJSON()`:
```json
{
  "session_id": "string",
  "user_id": "string", 
  "input_text": "string",
  "input_start_time": 1234567890,
  "input_end_time": 1234567890,
  "input_sent_time": 1234567890
}
```

### POST `/feedback`
Handles user feedback. Expects data matching `Feedback.toJSON()`:
```json
{
  "session_id": "string",
  "user_id": "string",
  "response_text": "string",
  "response_start_time": 1234567890,
  "response_end_time": 1234567890,
  "response_duration": 1000,
  "feedback_type": "positive|negative",
  "feedback_time": 1234567890,
  "feedback_delay_duration": 500
}
```

### POST `/session`
Handles session data. Expects data matching `Session.toJSON()`:
```json
{
  "session_id": "string",
  "user_id": "string",
  "session_start": 1234567890,
  "session_end": 1234567890,
  "session_end_type": "userAction",
  "session_duration": 10000
}
```

## 🧪 Testing

Run the test script to verify all endpoints work:

```bash
python test_ui_integration.py
```

This will test:
- ✅ Root endpoint
- ✅ UserPrompt endpoint with exact schema
- ✅ Feedback endpoint with exact schema  
- ✅ Session endpoint with exact schema
- ✅ API key authentication

## 🔒 Authentication

All endpoints require a valid Bearer token in the Authorization header:

```
Authorization: Bearer your-api-key-here
```

## 📊 Data Preservation

The backend preserves **ALL** original data from the UI:
- Every field from the JSON schemas is stored
- Metrics are extracted and analyzed
- User profiles are updated based on interaction patterns
- RL agent learns from the complete data

## 🚨 Troubleshooting

### Backend Not Starting
- Check if port 8000 is available
- Verify Python dependencies are installed
- Check environment variable `HUMANE_API_KEY` is set

### UI Not Connecting
- Verify backend is running on the configured URL
- Check API key matches between UI and backend
- Look for CORS errors in browser console

### Authentication Errors
- Ensure API key is set correctly
- Check Authorization header format: `Bearer <key>`
- Verify the key matches `HUMANE_API_KEY` environment variable

## 🔄 Development

### Adding New Endpoints
1. Update `main.py` with new endpoint
2. Update `dialogue_manager.py` to handle the data
3. Update test script to verify functionality

### Modifying Data Schemas
1. Update the Pydantic models in `main.py`
2. Update the processing logic in `dialogue_manager.py`
3. Update the test data in `test_ui_integration.py`

## 📝 Notes

- The backend automatically creates user profiles for new users
- RL agents are initialized per user for personalized responses
- All metrics and interactions are logged for analysis
- The system falls back to OpenAI integration if RL fails
