"""Demo script for the LangGraph AI agent."""
from main import create_agent_graph, run_agent
from config import validate_config

def demo_agent():
    """Demonstrate the agent workflow."""
    print("🎬 LangGraph AI Agent Demo")
    print("=" * 50)
    
    # Check configuration
    if not validate_config():
        print("❌ Please set up your .env file with OPENAI_API_KEY")
        print("   Copy env_example.txt to .env and add your API key")
        return
    
    # Create the agent
    app = create_agent_graph()
    
    # Test messages
    test_messages = [
        "Hello! How are you?",
        "What is the capital of France?",
        "Can you help me with a math problem?",
        "Tell me a joke!"
    ]
    
    print("🧪 Running test messages...")
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n--- Test {i} ---")
        result = run_agent(message, app)
        print(f"🤖 AI Response: {result['ai_response']}")
        print(f"📊 Messages in history: {len(result['messages'])}")
    
    print("\n🎉 Demo completed!")
    print("\nTo run interactive chat: python main.py")
    print("To run single message: python main.py 'Your message here'")

if __name__ == "__main__":
    demo_agent()
