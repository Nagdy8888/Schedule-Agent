"""Main entry point for the LangGraph AI agent."""
from langgraph.graph import StateGraph, END
from state import AgentState
from nodes import add_user_message, generate_ai_response, add_ai_message, send_gmail_message, should_send_email
from config import validate_config
from memory import get_memory


def create_agent_graph():
    """Create the LangGraph agent workflow."""
    print("Building LangGraph workflow...")
    
    # Initialize the graph with our state
    workflow = StateGraph(AgentState)
    
    # Add nodes to the graph
    workflow.add_node("add_user_message", add_user_message)
    workflow.add_node("generate_ai_response", generate_ai_response)
    workflow.add_node("add_ai_message", add_ai_message)
    workflow.add_node("send_gmail_message", send_gmail_message)
    
    # Set the entry point
    workflow.set_entry_point("add_user_message")
    
    # Connect the nodes with conditional routing
    # Flow: User Input → AI Response → Store Response → Check Email → Send Email (if needed) → END
    workflow.add_edge("add_user_message", "generate_ai_response")
    workflow.add_edge("generate_ai_response", "add_ai_message")
    
    # Add conditional edge for email sending
    workflow.add_conditional_edges(
        "add_ai_message",
        should_send_email,
        {
            True: "send_gmail_message",
            False: END
        }
    )
    
    workflow.add_edge("send_gmail_message", END)
    
    # Compile the graph
    app = workflow.compile()
    
    print("SUCCESS: LangGraph workflow created successfully!")
    return app


def run_agent(user_input: str, app=None):
    """Run the agent with a user input."""
    if app is None:
        app = create_agent_graph()
    
    print(f"\nStarting agent with input: '{user_input}'")
    print("=" * 50)
    
    # Create initial state
    initial_state = {
        "user_input": user_input,
        "ai_response": "",
        "messages": [],
        "to_email": "recipient@example.com",  # Default email
        "email_subject": "Message from AI Agent",
        "email_sent": False,
        "email_content": "",
        "is_complete": False,
        "needs_email": False
    }
    
    # Run the graph
    result = app.invoke(initial_state)
    
    print("=" * 50)
    print("Agent execution completed!")
    print(f"Total messages: {len(result['messages'])}")
    print(f"Complete: {result['is_complete']}")
    
    # Show email status
    if result.get('email_sent', False):
        print(f"Email sent: {result['email_content']}")
    else:
        print("No email sent")
    
    # Show memory stats
    memory = get_memory()
    stats = memory.get_memory_stats()
    print(f"Memory: {stats['total_messages']} total messages stored")
    
    return result


def interactive_chat():
    """Run an interactive chat session."""
    print("LangGraph AI Agent - Interactive Chat")
    print("Type 'quit' to exit")
    print("=" * 50)
    
    # Validate configuration
    if not validate_config():
        print("ERROR: Please set up your .env file with OPENAI_API_KEY")
        return
    
    # Create the agent
    app = create_agent_graph()
    
    # Interactive loop
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye!")
                break
            
            if not user_input:
                print("Please enter a message.")
                continue
            
            # Run the agent
            result = run_agent(user_input, app)
            
            # Display the AI response
            print(f"\nAI: {result['ai_response']}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    # Check if we want interactive mode or single run
    import sys
    
    if len(sys.argv) > 1:
        # Single run mode
        user_input = " ".join(sys.argv[1:])
        result = run_agent(user_input)
        print(f"\nAI: {result['ai_response']}")
    else:
        # Interactive mode
        interactive_chat()