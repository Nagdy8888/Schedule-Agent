"""Alternative nodes using SMTP instead of Gmail API."""
from datetime import datetime
from typing import Dict, Any
from state import AgentState, ChatMessage
from openai_service import get_openai_service
from memory import get_memory
from smtp_service import get_smtp_service

# Import all the original nodes
from nodes import add_user_message, generate_ai_response, add_ai_message, should_send_email

def send_smtp_message(state: AgentState) -> AgentState:
    """Node 4: Send email via SMTP (no OAuth required)."""
    print(f"📧 Sending email via SMTP...")
    
    try:
        # Get SMTP service
        smtp_service = get_smtp_service()
        
        if not smtp_service.is_available():
            print("❌ SMTP service not available. Please check credentials.")
            state["email_sent"] = False
            state["email_content"] = "SMTP service not available"
            return state
        
        # Extract email details from state
        to_email = state.get("to_email", "recipient@example.com")
        subject = state.get("email_subject", "Message from AI Agent")
        body = state["ai_response"]
        
        # Send email
        success = smtp_service.send_email(
            to=to_email,
            subject=subject,
            body=body
        )
        
        if success:
            state["email_sent"] = True
            state["email_content"] = f"Email sent to {to_email}: {subject}"
            print(f"✅ Email sent successfully to {to_email}")
        else:
            state["email_sent"] = False
            state["email_content"] = "Failed to send email"
            print("❌ Failed to send email")
    
    except Exception as e:
        print(f"❌ Error in send_smtp_message: {str(e)}")
        state["email_sent"] = False
        state["email_content"] = f"Error: {str(e)}"
    
    return state
