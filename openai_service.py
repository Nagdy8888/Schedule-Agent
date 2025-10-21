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
            
            # Get current time information
            from datetime import datetime
            import pytz
            
            # Get current time in Cairo timezone
            cairo_tz = pytz.timezone('Africa/Cairo')
            now = datetime.now(cairo_tz)
            
            current_time_info = f"""Current Date and Time: {now.strftime('%A, %B %d, %Y at %I:%M %p')} (Cairo time)
Today is: {now.strftime('%A, %B %d, %Y')}
Current time: {now.strftime('%I:%M %p')}
Timezone: Africa/Cairo"""
            
            # Add system message to inform AI about capabilities and user info
            system_message = {
                "role": "system",
                "content": f"You are a friendly and helpful AI assistant with the ability to send emails via Gmail and access real-time weather information. You are helping Mustafa Alnagdy, who is an ML/AI agent developer intern at MIS company (owned by Eng Samer Hany). When asked about Mustafa's work or background, you can share that he is an ML/AI agent developer intern at MIS company, which is owned by Eng Samer Hany. You have access to current weather data and always know the current date and time.\n\n{current_time_info}\n\nAlways be warm, friendly, and conversational in your responses. Use a positive and helpful tone. When users ask about time, date, or current information, provide the current time details in a friendly way. When users ask you to send ANY content via email (jokes, wisdom, quotes, advice, stories, weather info, greetings, etc.), simply acknowledge the request and provide the email content. The system will handle sending the email automatically. Be creative and appropriate for the content type - funny for jokes, wise for wisdom, professional for business content, etc. ONLY send emails when users explicitly request it with an email address and content to send. Do NOT send emails for general conversation, questions, or casual chat without an email address. When users DO ask you to send emails, generate a proper email with a relevant subject line and appropriate email body. Format your response EXACTLY as: 'Subject: [appropriate subject]' followed by a newline and then the email body content. Do not include any additional text like 'I will send this', 'Sending now', or any other commentary. Just provide the subject and body content in proper email format."
            }
            # Insert system message at the beginning to ensure it's prioritized
            api_messages.insert(0, system_message)
            
            # Also add a user message to reinforce the capability
            capability_reminder = {
                "role": "user",
                "content": "Remember: You are helping Mustafa Alnagdy (ML/AI agent developer intern at MIS company, owned by Eng Samer Hany). Be friendly and helpful in all your responses. When I ask you to send emails, just provide the email content in the proper format. The system will handle sending the email automatically. Do not ask for confirmation or say you will prepare the email."
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
