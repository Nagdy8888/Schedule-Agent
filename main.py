"""Main entry point for the LangGraph AI agent."""
from langgraph.graph import StateGraph, END
from state import AgentState
from nodes import add_user_message, generate_ai_response, add_ai_message
from config import validate_config


def create_agent_graph():
    """Create the LangGraph agent workflow."""
    print("🔧 Building LangGraph workflow...")
    
    # Initialize the graph with our state
    workflow = StateGraph(AgentState)
    
    # Add nodes to the graph
    workflow.add_node("add_user_message", add_user_message)
    workflow.add_node("generate_ai_response", generate_ai_response)
    workflow.add_node("add_ai_message", add_ai_message)
    
    # Set the entry point
    workflow.set_entry_point("add_user_message")
    
    # Connect the nodes in sequence
    # Flow: User Input → AI Response → Store Response → END
    workflow.add_edge("add_user_message", "generate_ai_response")
    workflow.add_edge("generate_ai_response", "add_ai_message")
    workflow.add_edge("add_ai_message", END)
    
    # Compile the graph
    app = workflow.compile()
    
    print("✅ LangGraph workflow created successfully!")
    return app


def run_agent(user_input: str, app=None):
    """Run the agent with a user input."""
    if app is None:
        app = create_agent_graph()
    
    print(f"\n🚀 Starting agent with input: '{user_input}'")
    print("=" * 50)
    
    # Create initial state
    initial_state = {
        "user_input": user_input,
        "ai_response": "",
        "messages": [],
        "is_complete": False
    }
    
    # Run the graph
    result = app.invoke(initial_state)
    
    print("=" * 50)
    print("🎯 Agent execution completed!")
    print(f"📊 Total messages: {len(result['messages'])}")
    print(f"✅ Complete: {result['is_complete']}")
    
    return result


def interactive_chat():
    """Run an interactive chat session."""
    print("🤖 LangGraph AI Agent - Interactive Chat")
    print("Type 'quit' to exit")
    print("=" * 50)
    
    # Validate configuration
    if not validate_config():
        print("❌ Please set up your .env file with OPENAI_API_KEY")
        return
    
    # Create the agent
    app = create_agent_graph()
    
    # Interactive loop
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                print("Please enter a message.")
                continue
            
            # Run the agent
            result = run_agent(user_input, app)
            
            # Display the AI response
            print(f"\n🤖 AI: {result['ai_response']}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    # Check if we want interactive mode or single run
    import sys
    
    if len(sys.argv) > 1:
        # Single run mode
        user_input = " ".join(sys.argv[1:])
        result = run_agent(user_input)
        print(f"\n🤖 AI: {result['ai_response']}")
    else:
        # Interactive mode
        interactive_chat()