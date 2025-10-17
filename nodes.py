"""Node functions for the basic AI agent."""
from datetime import datetime
from typing import Dict, Any
from state import AgentState, ChatMessage
from openai_service import get_openai_service
from memory import get_memory


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
    
    # Load memory and add to current conversation
    memory = get_memory()
    all_messages = memory.get_messages() + state["messages"]
    state["messages"] = all_messages
    
    # Save user message to memory
    memory.add_message(user_message)
    memory.save_memory()
    
    print(f"✅ User message stored. Total messages: {len(state['messages'])}")
    return state


def generate_ai_response(state: AgentState) -> AgentState:
    """Node 2: Use OpenAI to generate response."""
    print(f"🤖 Generating AI response for: {state['user_input']}")
    
    try:
        # Get OpenAI service
        openai_service = get_openai_service()
        
        # Generate response using OpenAI
        ai_response = openai_service.generate_response(
            messages=state["messages"],
            user_input=state["user_input"]
        )
        
    except Exception as e:
        print(f"❌ Error in generate_ai_response: {str(e)}")
        # Fallback response if OpenAI fails
        ai_response = f"I received your message: '{state['user_input']}'. However, I'm having trouble connecting to my AI service right now."
    
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
    
    # Save AI message to memory
    memory = get_memory()
    memory.add_message(ai_message)
    memory.save_memory()
    
    # Mark as complete
    state["is_complete"] = True
    
    print(f"✅ AI message stored. Total messages: {len(state['messages'])}")
    print(f"🎯 Conversation complete: {state['is_complete']}")
    return state