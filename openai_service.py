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
        
        print("✅ OpenAI client initialized successfully")
    
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
            print(f"🤖 Calling OpenAI API with {len(messages)} messages")
            
            # Format messages for OpenAI API
            api_messages = self.format_messages_for_api(messages)
            
            # Add the current user input
            api_messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=api_messages,
                temperature=self.temperature,
                max_tokens=500
            )
            
            # Extract the response content
            ai_response = response.choices[0].message.content
            
            print(f"✅ OpenAI response generated: {ai_response[:50]}...")
            return ai_response
            
        except Exception as e:
            error_msg = f"❌ Error calling OpenAI API: {str(e)}"
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
