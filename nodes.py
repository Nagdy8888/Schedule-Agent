"""Node functions for the basic AI agent."""
from datetime import datetime
from typing import Dict, Any
from state import AgentState, ChatMessage
from openai_service import get_openai_service


def add_user_message(state: AgentState) -> AgentState:
    """Node 1: Store the user's input in chat history."""
    print(f"📝 Adding user message: {state['user_input']}")
    
    user_message = ChatMessage(
        role="human",
        content=state["user_input"],
        timestamp=datetime.now().isoformat()
    )
    
    # Add to messages list
    state["messages"].append(user_message)
    
    print(f"✅ User message stored. Total messages: {len(state['messages'])}")
    return state


def generate_ai_response(state: AgentState) -> AgentState:
    """Node 2: Use OpenAI to generate response."""
    print(f"🤖 Generating AI response for: {state['user_input']}")
    
    # For now, create a simple response (we'll add OpenAI in Step 3)
    ai_response = f"I received your message: '{state['user_input']}'. This is a placeholder response from the AI agent!"
    
    # Store the response in state
    state["ai_response"] = ai_response
    
    print(f"✅ AI response generated: {ai_response[:50]}...")
    return state


def add_ai_message(state: AgentState) -> AgentState:
    """Node 3: Store the AI's response in chat history."""
    print(f"💾 Storing AI response in chat history")
    
    ai_message = ChatMessage(
        role="ai",
        content=state["ai_response"],
        timestamp=datetime.now().isoformat()
    )
    
    # Add to messages list
    state["messages"].append(ai_message)
    
    # Mark as complete
    state["is_complete"] = True
    
    print(f"✅ AI message stored. Total messages: {len(state['messages'])}")
    print(f"🎯 Conversation complete: {state['is_complete']}")
    return state