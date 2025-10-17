"""Memory management utilities for the LangGraph agent."""
from memory import get_memory
import json

def show_memory_stats():
    """Display memory statistics."""
    memory = get_memory()
    stats = memory.get_memory_stats()
    
    print("📊 Memory Statistics")
    print("=" * 40)
    print(f"Total Messages: {stats['total_messages']}")
    print(f"Human Messages: {stats['human_messages']}")
    print(f"AI Messages: {stats['ai_messages']}")
    print(f"Last Updated: {stats['last_updated']}")

def show_recent_messages(count: int = 5):
    """Show recent messages from memory."""
    memory = get_memory()
    recent = memory.get_recent_messages(count)
    
    print(f"📝 Recent {len(recent)} Messages")
    print("=" * 40)
    
    for i, msg in enumerate(recent, 1):
        role_emoji = "👤" if msg['role'] == 'human' else "🤖"
        print(f"{i}. {role_emoji} {msg['role'].upper()}: {msg['content']}")
        print(f"   ⏰ {msg['timestamp']}")
        print()

def show_full_memory():
    """Show all messages from memory."""
    memory = get_memory()
    messages = memory.get_messages()
    
    print(f"📚 Full Memory ({len(messages)} messages)")
    print("=" * 50)
    
    for i, msg in enumerate(messages, 1):
        role_emoji = "👤" if msg['role'] == 'human' else "🤖"
        print(f"{i}. {role_emoji} {msg['role'].upper()}: {msg['content']}")
        print(f"   ⏰ {msg['timestamp']}")
        print()

def clear_memory():
    """Clear all memory."""
    memory = get_memory()
    memory.clear_memory()
    print("🗑️ Memory cleared successfully!")

def export_memory(filename: str = "memory_export.json"):
    """Export memory to a JSON file."""
    memory = get_memory()
    messages = memory.get_messages()
    
    export_data = {
        'export_date': memory.get_memory_stats()['last_updated'],
        'total_messages': len(messages),
        'messages': messages
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"📤 Memory exported to {filename}")

def main():
    """Main memory management interface."""
    import sys
    
    if len(sys.argv) < 2:
        print("Memory Management Commands:")
        print("  python memory_manager.py stats     - Show memory statistics")
        print("  python memory_manager.py recent    - Show recent messages")
        print("  python memory_manager.py full      - Show all messages")
        print("  python memory_manager.py clear     - Clear all memory")
        print("  python memory_manager.py export    - Export memory to JSON")
        return
    
    command = sys.argv[1].lower()
    
    if command == "stats":
        show_memory_stats()
    elif command == "recent":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        show_recent_messages(count)
    elif command == "full":
        show_full_memory()
    elif command == "clear":
        confirm = input("Are you sure you want to clear all memory? (y/N): ")
        if confirm.lower() == 'y':
            clear_memory()
        else:
            print("Memory not cleared.")
    elif command == "export":
        filename = sys.argv[2] if len(sys.argv) > 2 else "memory_export.json"
        export_memory(filename)
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
