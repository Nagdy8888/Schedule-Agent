"""Memory system for storing chat history in JSON file."""
import json
import os
from datetime import datetime
from typing import List, Dict, Any
from state import ChatMessage, AgentState


class ChatMemory:
    """Simple memory system that stores chat history in JSON file."""
    
    def __init__(self, memory_file: str = "chat_memory.json"):
        """Initialize memory with JSON file."""
        self.memory_file = memory_file
        self.messages = []
        self.load_memory()
    
    def load_memory(self):
        """Load chat history from JSON file."""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.messages = data.get('messages', [])
                print(f"Loaded {len(self.messages)} messages from memory")
            else:
                print("No existing memory found, starting fresh")
                self.messages = []
        except Exception as e:
            print(f"ERROR loading memory: {str(e)}")
            self.messages = []
    
    def save_memory(self):
        """Save chat history to JSON file."""
        try:
            memory_data = {
                'last_updated': datetime.now().isoformat(),
                'total_messages': len(self.messages),
                'messages': self.messages
            }
            
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, indent=2, ensure_ascii=False)
            
            print(f"Saved {len(self.messages)} messages to memory")
        except Exception as e:
            print(f"ERROR saving memory: {str(e)}")
    
    def add_message(self, message: ChatMessage):
        """Add a message to memory."""
        self.messages.append(message)
        print(f"Added message to memory: {message['role']} - {message['content'][:50]}...")
    
    def add_messages(self, messages: List[ChatMessage]):
        """Add multiple messages to memory."""
        self.messages.extend(messages)
        print(f"Added {len(messages)} messages to memory")
    
    def get_messages(self) -> List[ChatMessage]:
        """Get all messages from memory."""
        return self.messages
    
    def get_recent_messages(self, count: int = 10) -> List[ChatMessage]:
        """Get recent messages from memory."""
        return self.messages[-count:] if self.messages else []
    
    def clear_memory(self):
        """Clear all messages from memory."""
        self.messages = []
        self.save_memory()
        print("Memory cleared")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        human_messages = [msg for msg in self.messages if msg['role'] == 'human']
        ai_messages = [msg for msg in self.messages if msg['role'] == 'ai']
        
        return {
            'total_messages': len(self.messages),
            'human_messages': len(human_messages),
            'ai_messages': len(ai_messages),
            'last_updated': datetime.now().isoformat()
        }


# Global memory instance
chat_memory = None

def get_memory() -> ChatMemory:
    """Get or create memory instance."""
    global chat_memory
    if chat_memory is None:
        chat_memory = ChatMemory()
    return chat_memory


def save_conversation_to_memory(state: AgentState):
    """Save the current conversation to memory."""
    memory = get_memory()
    
    # Get the last two messages (user + AI response)
    if len(state['messages']) >= 2:
        recent_messages = state['messages'][-2:]
        memory.add_messages(recent_messages)
        memory.save_memory()
    
    return state
