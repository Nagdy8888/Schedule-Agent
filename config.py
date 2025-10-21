"""Configuration settings for the LangGraph agent."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Gmail API
GMAIL_CREDENTIALS_FILE = os.getenv("GMAIL_CREDENTIALS_FILE", "gmail.json")
GMAIL_TOKEN_FILE = os.getenv("GMAIL_TOKEN_FILE", "token.json")

# Weather API URL
WEATHER_API_URL = os.getenv("WEATHER_API_KEY")

# Model configuration
DEFAULT_MODEL = "gpt-4o"
DEFAULT_TEMPERATURE = 0.7

# Validation
def validate_config():
    """Validate that required configuration is present."""
    if not OPENAI_API_KEY:
        print("⚠️  Warning: OPENAI_API_KEY not found in environment variables")
        print("   Please create a .env file with your OpenAI API key")
        return False
    return True