"""
Main application for HumAIne-chatbot

This is the entry point for the HumAIne-chatbot system, providing
a FastAPI-based web service for the personalized conversational AI.
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import our core modules
from src.core.dialogue_manager import DialogueManager
from src.core.user_profiler import UserProfiler
from src.core.metrics_collector import MetricsCollector
from src.core.openai_integration import OpenAIIntegration
from src.models.schemas import UserPromptSimple

app = FastAPI(title="HumAIne Chatbot API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core services
user_profiler = UserProfiler()
metrics_collector = MetricsCollector()
openai_integration = OpenAIIntegration()  # Will now use OPENAI_API_KEY from .env
dialogue_manager = DialogueManager(
    user_profiler=user_profiler,
    metrics_collector=metrics_collector,
    openai_integration=openai_integration
)

# Get API key from environment variable
API_KEY = os.getenv("HUMANE_API_KEY", "test-api-key-123")

def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.replace("Bearer ", "")
    if token != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return token

# Pydantic models matching EXACTLY what the UI sends
class UserPromptSimple(BaseModel):
    """Simplified User Prompt Schema - matches exactly what the UI sends"""
    session_id: str
    user_id: str
    input_text: str
    input_start_time: int
    input_end_time: int
    input_sent_time: int
    
    # Additional metrics from userMessage.metrics may be included dynamically
    # These are optional and not required by the schema
    class Config:
        extra = "allow"  # Allow additional fields from UI metrics

class FeedbackRequest(BaseModel):
    session_id: str
    user_id: str
    response_text: str
    response_start_time: int
    response_end_time: int
    response_duration: int
    feedback_type: str
    feedback_time: int
    feedback_delay_duration: int

class SessionRequest(BaseModel):
    session_id: str
    user_id: str
    session_start: int
    session_end: Optional[int] = None
    session_end_type: Optional[str] = None
    session_duration: int
    # Additional metrics will be included dynamically
    class Config:
        extra = "allow"  # Allow additional fields from UI metrics

class ChatResponse(BaseModel):
    message: str
    success: bool = True

@app.get("/")
async def root():
    return {"message": "HumAIne Chatbot API is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint with OpenAI connectivity status"""
    try:
        # Check OpenAI connectivity
        openai_status = openai_integration.check_connectivity()
        
        # Safely get active conversations count
        try:
            active_conversations = len(dialogue_manager.active_conversations)
        except AttributeError:
            active_conversations = 0
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "openai": openai_status,
            "active_conversations": active_conversations,
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e),
            "version": "1.0.0"
        }

@app.get("/profile/{user_id}")
async def get_user_profile(user_id: str, token: str = Depends(verify_token)):
    """Get user profile and insights"""
    try:
        profile = user_profiler.get_user_profile(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        # Get cross-session insights
        insights = user_profiler.get_user_insights(user_id)
        
        return {
            "user_id": user_id,
            "profile": {
                "preferred_language_complexity": profile.preferred_language_complexity,
                "preferred_detail_level": profile.preferred_detail_level,
                "preferred_response_style": profile.preferred_response_style,
                "average_session_duration": profile.average_session_duration,
                "average_response_time": profile.average_response_time,
                "average_typing_speed": profile.average_typing_speed,
                "average_sentiment_score": profile.average_sentiment_score,
                "average_language_complexity": profile.average_language_complexity,
                "average_grammatical_accuracy": profile.average_grammatical_accuracy,
                "total_sessions": profile.total_sessions,
                "average_engagement_time": profile.average_engagement_time,
                "feedback_ratio": profile.feedback_ratio,
                "positive_feedback_ratio": profile.positive_feedback_ratio,
                "created_at": profile.created_at.isoformat(),
                "updated_at": profile.updated_at.isoformat()
            },
            "insights": insights,
            "session_count": len(profile.session_history),
            "feedback_count": len(profile.feedback_history)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving profile: {str(e)}")

@app.get("/profiles/stats")
async def get_profile_stats(token: str = Depends(verify_token)):
    """Get statistics about all user profiles"""
    try:
        stats = user_profiler.get_profile_stats()
        return {
            "status": "success",
            "stats": stats,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving profile stats: {str(e)}")

@app.get("/profiles/insights/{user_id}")
async def get_user_insights(user_id: str, token: str = Depends(verify_token)):
    """Get detailed insights for a specific user"""
    try:
        insights = user_profiler.get_user_insights(user_id)
        if not insights:
            raise HTTPException(status_code=404, detail="No insights available for this user")
        
        return {
            "user_id": user_id,
            "insights": insights,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving insights: {str(e)}")

@app.post("/profiles/save")
async def save_all_profiles(token: str = Depends(verify_token)):
    """Save all profiles to disk"""
    try:
        success = user_profiler.save_all_profiles()
        if success:
            return {
                "status": "success",
                "message": "All profiles saved successfully",
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to save profiles")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving profiles: {str(e)}")

@app.post("/interact")
async def interact(user_prompt: UserPromptSimple, token: str = Depends(verify_token)):
    """Handle user message and return chatbot response - matches UserPrompt.toJSON() schema exactly"""
    try:
        # Convert to our internal format - preserving ALL original data
        prompt_data = {
            "session_id": user_prompt.session_id,
            "user_id": user_prompt.user_id,
            "input_text": user_prompt.input_text,
            "input_start_time": user_prompt.input_start_time,
            "input_end_time": user_prompt.input_end_time,
            "input_sent_time": user_prompt.input_sent_time
        }
        
        # Get response from dialogue manager
        response = await dialogue_manager.process_user_input(prompt_data)
        
        return ChatResponse(message=response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.post("/feedback")
async def feedback(feedback_data: FeedbackRequest, token: str = Depends(verify_token)):
    """Handle user feedback - matches Feedback.toJSON() schema exactly"""
    try:
        # Convert Pydantic model to dictionary - preserving ALL the original data
        feedback_dict = feedback_data.model_dump()
        
        # Process feedback
        await dialogue_manager.process_feedback(feedback_dict)
        return ChatResponse(message="Feedback received successfully")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing feedback: {str(e)}")

@app.post("/session")
async def session(session_data: SessionRequest, token: str = Depends(verify_token)):
    """Handle session data - matches Session.toJSON() schema exactly"""
    try:
        # Convert Pydantic model to dictionary - preserving ALL the original data
        session_dict = session_data.model_dump()
        
        # Process session
        await dialogue_manager.process_session(session_dict)
        return ChatResponse(message="Session processed successfully")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing session: {str(e)}")

@app.get("/metrics/engagement/{user_id}")
async def get_user_engagement_metrics(user_id: str, token: str = Depends(verify_token)):
    """Get real-time engagement metrics for a user"""
    try:
        engagement_metrics = metrics_collector.get_real_time_engagement_metrics(user_id)
        return {
            "status": "success",
            "user_id": user_id,
            "engagement_metrics": engagement_metrics,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving engagement metrics: {str(e)}")

@app.get("/metrics/behavior/{user_id}")
async def get_user_behavior_metrics(user_id: str, token: str = Depends(verify_token)):
    """Get user behavior analysis for a user"""
    try:
        behavior_metrics = metrics_collector.get_user_behavior_analysis(user_id)
        return {
            "status": "success",
            "user_id": user_id,
            "behavior_metrics": behavior_metrics,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving behavior metrics: {str(e)}")

@app.get("/metrics/comprehensive/{user_id}")
async def get_comprehensive_user_metrics(user_id: str, token: str = Depends(verify_token)):
    """Get comprehensive metrics for a user including real-time and historical data"""
    try:
        comprehensive_metrics = metrics_collector.get_comprehensive_user_metrics(user_id)
        return {
            "status": "success",
            "user_id": user_id,
            "comprehensive_metrics": comprehensive_metrics,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving comprehensive metrics: {str(e)}")

@app.get("/metrics/overview")
async def get_metrics_overview(token: str = Depends(verify_token)):
    """Get overview of all metrics across the system"""
    try:
        active_sessions = metrics_collector.get_active_sessions()
        total_users = len(set(session.get('user_id') for session in active_sessions.values()))
        total_sessions = len(active_sessions)
        
        overview = {
            "total_active_users": total_users,
            "total_active_sessions": total_sessions,
            "system_health": "healthy",
            "metrics_summary": {
                "sessions_tracked": total_sessions,
                "users_tracked": total_users,
                "data_collection_active": True
            }
        }
        
        return {
            "status": "success",
            "overview": overview,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving metrics overview: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 