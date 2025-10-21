"""State management for the basic AI agent."""
from typing import List, Dict, Any
from typing_extensions import TypedDict


class ChatMessage(TypedDict):
    """Structure for a chat message."""
    role: str  # "human" or "ai"
    content: str
    timestamp: str


class AgentState(TypedDict):
    """Main state for the basic AI agent."""
    # Current conversation
    user_input: str
    ai_response: str
    
    # Chat history for memory
    messages: List[ChatMessage]
    
    # Email functionality
    to_email: str
    email_subject: str
    email_sent: bool
    email_content: str
    
    # Weather functionality
    weather_data: Dict[str, Any]
    weather_summary: str
    needs_weather: bool
    
    # Time functionality
    time_data: Dict[str, Any]
    time_summary: str
    needs_time: bool
    
    # Control flow
    is_complete: bool
    needs_email: bool