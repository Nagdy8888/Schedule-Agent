"""Node functions for the basic AI agent."""
from datetime import datetime
from typing import Dict, Any
from state import AgentState, ChatMessage
from openai_service import get_openai_service
from memory import get_memory
from gmail_service import get_gmail_service


def add_user_message(state: AgentState) -> AgentState:
    """Node 1: Store the user's input in chat history."""
    print(f"Adding user message: {state['user_input']}")
    
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
    
    print(f"SUCCESS: User message stored. Total messages: {len(state['messages'])}")
    return state


def generate_ai_response(state: AgentState) -> AgentState:
    """Node 2: Use OpenAI to generate response."""
    print(f"Generating AI response for: {state['user_input']}")
    
    try:
        # Get OpenAI service
        openai_service = get_openai_service()
        
        # Generate response using OpenAI
        ai_response = openai_service.generate_response(
            messages=state["messages"],
            user_input=state["user_input"]
        )
        
    except Exception as e:
        print(f"ERROR in generate_ai_response: {str(e)}")
        # Fallback response if OpenAI fails
        ai_response = f"I received your message: '{state['user_input']}'. However, I'm having trouble connecting to my AI service right now."
    
    # Store the response in state
    state["ai_response"] = ai_response
    
    print(f"SUCCESS: AI response generated: {ai_response[:50]}...")
    return state


def add_ai_message(state: AgentState) -> AgentState:
    """Node 3: Store the AI's response in chat history."""
    print(f"Storing AI response in chat history")
    
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
    
    print(f"SUCCESS: AI message stored. Total messages: {len(state['messages'])}")
    print(f"Conversation complete: {state['is_complete']}")
    return state


def send_gmail_message(state: AgentState) -> AgentState:
    """Node 4: Send email via Gmail."""
    print(f"Sending Gmail message...")
    
    try:
        # Get Gmail service
        gmail_service = get_gmail_service()
        
        if not gmail_service.is_available():
            print("ERROR: Gmail service not available. Please check credentials.")
            state["email_sent"] = False
            state["email_content"] = "Gmail service not available"
            return state
        
        # Extract email details from user input
        user_input = state["user_input"].lower()
        
        # Try to extract email address from user input
        import re
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_matches = re.findall(email_pattern, state["user_input"])
        
        if email_matches:
            to_email = email_matches[0]  # Use the first email found
            print(f"Found email in message: {to_email}")
        else:
            # Default email if none found
            to_email = "recipient@example.com"
            print(f"No email found, using default: {to_email}")
        
        # Extract subject from user input or use default
        if "subject" in user_input or "title" in user_input:
            # Try to extract subject from user input
            subject_match = re.search(r'(?:subject|title)[\s:]+([^.!?]+)', user_input, re.IGNORECASE)
            if subject_match:
                subject = subject_match.group(1).strip()
            else:
                subject = "Message from AI Agent"
        else:
            subject = "Message from AI Agent"
        
        # Extract proper email content from AI response
        ai_response = state["ai_response"]
        
        # Try to extract the actual greeting/message content from AI response
        # Look for patterns like "Body: Hello!" or "Hello! I hope you are doing well!"
        body_patterns = [
            r'\*\*Body:\*\*\s*([^*]+?)(?:\*|$)',  # **Body:** Hello! I hope...
            r'Body:\s*([^*]+?)(?:\*|$)',  # Body: Hello! I hope...
            r'Hello![^!]*!',  # Hello! I hope you are doing well!
            r'Greeting[^!]*!',  # Greeting message
        ]
        
        body = ai_response  # Default to full response
        for pattern in body_patterns:
            match = re.search(pattern, ai_response, re.IGNORECASE | re.DOTALL)
            if match:
                body = match.group(1).strip() if match.groups() else match.group(0).strip()
                break
        
        # If no specific pattern found, try to extract a simple greeting
        if body == ai_response:  # No pattern matched
            # Look for simple greeting patterns
            greeting_patterns = [
                r'Hello![^!]*!',
                r'Hi[^!]*!',
                r'Greetings[^!]*!',
                r'I hope you are doing well[^!]*!',
            ]
            
            for pattern in greeting_patterns:
                match = re.search(pattern, ai_response, re.IGNORECASE)
                if match:
                    body = match.group(0).strip()
                    break
        
        # If still no good content, create a simple greeting based on user input
        if body == ai_response or len(body) < 10:
            if "greeting" in user_input.lower():
                body = "Hello! I hope you are doing well!"
            elif "hello" in user_input.lower():
                body = "Hello! How are you today?"
            else:
                body = "Hello! I hope this message finds you well."
        
        # Send email
        success = gmail_service.send_email(
            to=to_email,
            subject=subject,
            body=body
        )
        
        if success:
            state["email_sent"] = True
            state["email_content"] = f"Email sent to {to_email}: {subject}"
            print(f"SUCCESS: Email sent successfully to {to_email}")
        else:
            state["email_sent"] = False
            state["email_content"] = "Failed to send email"
            print("ERROR: Failed to send email")
    
    except Exception as e:
        print(f"ERROR in send_gmail_message: {str(e)}")
        state["email_sent"] = False
        state["email_content"] = f"Error: {str(e)}"
    
    return state


def should_send_email(state: AgentState) -> bool:
    """Determine if we should send an email based on user input."""
    # Simple keyword detection for email sending
    email_keywords = ["email", "send", "gmail", "mail", "message"]
    user_input_lower = state["user_input"].lower()
    
    return any(keyword in user_input_lower for keyword in email_keywords)