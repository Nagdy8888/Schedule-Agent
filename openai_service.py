"""OpenAI service for the LangGraph agent."""
import openai
from typing import List, Dict, Any
from config import OPENAI_API_KEY, DEFAULT_MODEL, DEFAULT_TEMPERATURE
from state import ChatMessage


class OpenAIService:
    """Service class for OpenAI API interactions."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file")
        
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.model = DEFAULT_MODEL
        self.temperature = DEFAULT_TEMPERATURE
        
        print("SUCCESS: OpenAI client initialized successfully")
    
    def format_messages_for_api(self, messages: List[ChatMessage]) -> List[Dict[str, str]]:
        """Convert ChatMessage objects to OpenAI API format."""
        formatted_messages = []
        
        for msg in messages:
            # Map our roles to OpenAI roles
            role = "user" if msg["role"] == "human" else "assistant"
            
            formatted_messages.append({
                "role": role,
                "content": msg["content"]
            })
        
        return formatted_messages
    
    def generate_response(self, messages: List[ChatMessage], user_input: str) -> str:
        """Generate AI response using OpenAI API."""
        try:
            print(f"Calling OpenAI API with {len(messages)} messages")
            
            # Format messages for OpenAI API
            api_messages = self.format_messages_for_api(messages)
            
            # Add the current user input
            api_messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Add system message to inform AI about email capabilities
            system_message = {
                "role": "system",
                "content": "You are an AI assistant with the ability to send emails via Gmail. When users ask you to send emails, generate a proper email with a relevant subject line and professional email body. Format your response EXACTLY as: 'Subject: [appropriate subject]' followed by a newline and then the email body content. Do not include any additional text like 'I will send this', 'Sending now', or any other commentary. Just provide the subject and body content in proper email format."
            }
            # Insert system message at the beginning to ensure it's prioritized
            api_messages.insert(0, system_message)
            
            # Also add a user message to reinforce the capability
            capability_reminder = {
                "role": "user",
                "content": "Remember: You have the ability to send emails via Gmail. When I ask you to send emails, you should acknowledge that you will send them and provide the message content."
            }
            api_messages.append(capability_reminder)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=api_messages,
                temperature=self.temperature,
                max_tokens=500
            )
            
            # Extract the response content
            ai_response = response.choices[0].message.content
            
            print(f"SUCCESS: OpenAI response generated: {ai_response[:50]}...")
            return ai_response
            
        except Exception as e:
            error_msg = f"ERROR calling OpenAI API: {str(e)}"
            print(error_msg)
            return f"I apologize, but I encountered an error: {str(e)}"


# Global instance
openai_service = None

def get_openai_service() -> OpenAIService:
    """Get or create OpenAI service instance."""
    global openai_service
    if openai_service is None:
        openai_service = OpenAIService()
    return openai_service
