"""Test script for OpenAI integration."""
from config import validate_config
from openai_service import get_openai_service
from state import ChatMessage

def test_openai_integration():
    """Test the OpenAI integration."""
    print("🧪 Testing OpenAI Integration...")
    
    # Check configuration
    if not validate_config():
        print("❌ Configuration validation failed")
        return False
    
    try:
        # Get OpenAI service
        openai_service = get_openai_service()
        
        # Create test messages
        test_messages = [
            ChatMessage(
                role="human",
                content="Hello!",
                timestamp="2025-01-01T00:00:00"
            )
        ]
        
        # Test response generation
        response = openai_service.generate_response(
            messages=test_messages,
            user_input="What is 2+2?"
        )
        
        print(f"✅ OpenAI test successful!")
        print(f"📝 Response: {response}")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_openai_integration()
