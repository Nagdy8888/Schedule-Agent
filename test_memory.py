"""Test script to verify memory stores both user and AI messages."""
from memory import get_memory
from state import ChatMessage
from datetime import datetime

def test_memory_storage():
    """Test that memory stores both user and AI messages."""
    print("🧪 Testing Memory Storage")
    print("=" * 40)
    
    # Get memory instance
    memory = get_memory()
    
    # Clear existing memory for clean test
    memory.clear_memory()
    
    # Create test messages
    user_message = ChatMessage(
        role="human",
        content="Hello, this is a test message from user",
        timestamp=datetime.now().isoformat()
    )
    
    ai_message = ChatMessage(
        role="ai",
        content="Hello! This is a test response from AI",
        timestamp=datetime.now().isoformat()
    )
    
    # Add messages to memory
    print("📝 Adding user message...")
    memory.add_message(user_message)
    memory.save_memory()
    
    print("📝 Adding AI message...")
    memory.add_message(ai_message)
    memory.save_memory()
    
    # Check what's stored
    stored_messages = memory.get_messages()
    stats = memory.get_memory_stats()
    
    print("\n📊 Memory Statistics:")
    print(f"Total Messages: {stats['total_messages']}")
    print(f"Human Messages: {stats['human_messages']}")
    print(f"AI Messages: {stats['ai_messages']}")
    
    print("\n📚 Stored Messages:")
    for i, msg in enumerate(stored_messages, 1):
        role_emoji = "👤" if msg['role'] == 'human' else "🤖"
        print(f"{i}. {role_emoji} {msg['role'].upper()}: {msg['content']}")
        print(f"   ⏰ {msg['timestamp']}")
    
    # Verify both types are stored
    human_count = len([msg for msg in stored_messages if msg['role'] == 'human'])
    ai_count = len([msg for msg in stored_messages if msg['role'] == 'ai'])
    
    if human_count > 0 and ai_count > 0:
        print("\n✅ SUCCESS: Both user and AI messages are being stored!")
    else:
        print("\n❌ FAILED: Not both message types are being stored")
        print(f"Human messages: {human_count}, AI messages: {ai_count}")

if __name__ == "__main__":
    test_memory_storage()
