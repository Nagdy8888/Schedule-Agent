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
    
    # Control flow
    is_complete: bool