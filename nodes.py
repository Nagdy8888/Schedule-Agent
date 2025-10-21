"""Node functions for the basic AI agent."""
import re
from datetime import datetime
from typing import Dict, Any
from state import AgentState, ChatMessage
from openai_service import get_openai_service
from memory import get_memory
from gmail_service import get_gmail_service
from weather_service import get_weather_service
from time_service import get_time_service


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
            print(f"No email found")
        
        # Extract subject from AI response first, then fallback to user input
        ai_response = state["ai_response"]
        
        # Try to extract subject from AI response
        subject_match = re.search(r'Subject:\s*([^\n\r]+)', ai_response, re.IGNORECASE)
        if subject_match:
            subject = subject_match.group(1).strip()
        else:
            # Fallback: extract from user input or use default
            if "subject" in user_input or "title" in user_input:
                user_subject_match = re.search(r'(?:subject|title)[\s:]+([^.!?]+)', user_input, re.IGNORECASE)
                if user_subject_match:
                    subject = user_subject_match.group(1).strip()
                else:
                    subject = "Message from AI Agent"
            else:
                subject = "Message from AI Agent"
        
        # Extract email body from AI response
        # Look for content after "Subject:" line, stopping at common ending phrases
        body_match = re.search(r'Subject:\s*[^\n\r]+\s*\n\s*(.+?)(?:\n\s*(?:I will send|Sending|I am sending|This will be sent).*)?$', ai_response, re.IGNORECASE | re.DOTALL)
        if body_match:
            body = body_match.group(1).strip()
        else:
            # Fallback: look for patterns like "Body:" or extract from common greeting patterns
            body_patterns = [
                r'Body:\s*([^*]+?)(?:\*|$)',  # Body: Hello! I hope...
                r'\*\*Body:\*\*\s*([^*]+?)(?:\*|$)',  # **Body:** Hello! I hope...
                r'Hello![^!]*!',  # Hello! I hope you are doing well!
                r'Hi[^!]*!',  # Hi! How are you?
                r'Greetings[^!]*!',  # Greeting message
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
    user_input_lower = state["user_input"].lower()
    
    # Only send emails when explicitly requested with specific patterns
    email_patterns = [
        r'send.*email.*to',
        r'send.*message.*to',
        r'send.*to.*@',
        r'email.*to.*@',
        r'message.*to.*@',
        r'send.*gmail.*to',
        r'write.*email.*to',
        r'compose.*email.*to'
    ]
    
    # Check for explicit email sending requests
    for pattern in email_patterns:
        if re.search(pattern, user_input_lower):
            return True
    
    # Also check for direct commands with email addresses
    if re.search(r'@\w+\.\w+', user_input_lower) and any(word in user_input_lower for word in ['send', 'email', 'message']):
        return True
    
    # Check for email requests without specific address (like "send email to my manager")
    if any(phrase in user_input_lower for phrase in ['send email to my', 'send message to my', 'email my', 'message my']):
        return True
    
    return False


def get_weather_info(state: AgentState) -> AgentState:
    """Node: Get current weather information."""
    print("Getting weather information...")
    
    try:
        # Initialize weather service
        weather_service = get_weather_service()
        print("SUCCESS: Weather service initialized successfully")
        
        # Get weather data
        weather_data = weather_service.get_current_weather()
        
        if "error" in weather_data:
            state["weather_data"] = weather_data
            state["weather_summary"] = f"Weather data unavailable: {weather_data['error']}"
            print(f"ERROR: {weather_data['error']}")
        else:
            # Get weather summary
            weather_summary = weather_service.get_weather_summary()
            
            state["weather_data"] = weather_data
            state["weather_summary"] = weather_summary
            print("SUCCESS: Weather data retrieved successfully")
            
    except Exception as e:
        print(f"ERROR in get_weather_info: {str(e)}")
        state["weather_data"] = {"error": f"Weather service error: {str(e)}"}
        state["weather_summary"] = f"Weather data unavailable: {str(e)}"
    
    return state


def should_get_weather(state: AgentState) -> bool:
    """Determine if we should get weather information based on user input."""
    user_input_lower = state["user_input"].lower()
    
    # Weather-related keywords
    weather_keywords = [
        "weather", "temperature", "rain", "sunny", "cloudy", "wind", 
        "humidity", "forecast", "climate", "storm", "snow", "hot", "cold"
    ]
    
    # Check for weather-related requests
    for keyword in weather_keywords:
        if keyword in user_input_lower:
            return True
    
    # Check for specific weather questions
    weather_questions = [
        "what's the weather", "how's the weather", "weather today",
        "current weather", "weather forecast", "is it raining",
        "is it sunny", "temperature outside"
    ]
    
    for question in weather_questions:
        if question in user_input_lower:
            return True
    
    return False


def check_email_routing(state: AgentState) -> AgentState:
    """Simple routing node to check if email should be sent."""
    return state


def check_time_routing(state: AgentState) -> AgentState:
    """Simple routing node to check if time should be retrieved."""
    return state


def get_time_info(state: AgentState) -> AgentState:
    """Node: Get current date and time information."""
    print("Getting time information...")
    
    try:
        # Initialize time service
        time_service = get_time_service()
        print("SUCCESS: Time service initialized successfully")
        
        # Get time data
        time_data = time_service.get_current_time()
        
        if "error" in time_data:
            state["time_data"] = time_data
            state["time_summary"] = f"Time data unavailable: {time_data['error']}"
            print(f"ERROR: {time_data['error']}")
        else:
            # Get time summary
            time_summary = time_service.get_time_summary()
            
            state["time_data"] = time_data
            state["time_summary"] = time_summary
            print("SUCCESS: Time data retrieved successfully")
            
    except Exception as e:
        print(f"ERROR in get_time_info: {str(e)}")
        state["time_data"] = {"error": f"Time service error: {str(e)}"}
        state["time_summary"] = f"Time data unavailable: {str(e)}"
    
    return state


def should_get_time(state: AgentState) -> bool:
    """Determine if we should get time information based on user input."""
    user_input_lower = state["user_input"].lower()
    
    # Time-related keywords
    time_keywords = [
        "time", "date", "today", "now", "current", "clock", "calendar",
        "day", "month", "year", "hour", "minute", "second", "weekday",
        "weekend", "morning", "afternoon", "evening", "night"
    ]
    
    # Check for time-related requests
    for keyword in time_keywords:
        if keyword in user_input_lower:
            return True
    
    # Check for specific time questions
    time_questions = [
        "what time is it", "what's the time", "current time", "what date is it",
        "what's the date", "current date", "what day is it", "what day is today",
        "what month is it", "what year is it", "when is it", "how late is it"
    ]
    
    for question in time_questions:
        if question in user_input_lower:
            return True
    
    return False