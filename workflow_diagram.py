"""Generate a visual diagram of the LangGraph workflow."""
from main import create_agent_graph

def show_workflow_diagram():
    """Display the workflow diagram."""
    print("📊 LangGraph Workflow Diagram")
    print("=" * 50)
    
    # Create the agent to get the graph
    app = create_agent_graph()
    
    # Get the graph representation
    graph = app.get_graph()
    
    print("🔄 Workflow Flow:")
    print("┌─────────────────┐")
    print("│  START          │")
    print("└─────────┬───────┘")
    print("          │")
    print("          ▼")
    print("┌─────────────────┐")
    print("│ add_user_message│ ◄── Store user input in chat history")
    print("└─────────┬───────┘")
    print("          │")
    print("          ▼")
    print("┌─────────────────┐")
    print("│generate_ai_resp │ ◄── Call OpenAI API to generate response")
    print("└─────────┬───────┘")
    print("          │")
    print("          ▼")
    print("┌─────────────────┐")
    print("│ add_ai_message  │ ◄── Store AI response in chat history")
    print("└─────────┬───────┘")
    print("          │")
    print("          ▼")
    print("┌─────────────────┐")
    print("│      END        │")
    print("└─────────────────┘")
    
    print("\n📝 Node Details:")
    print("• add_user_message: Takes user input, stores as 'human' message")
    print("• generate_ai_response: Calls OpenAI API with chat history")
    print("• add_ai_message: Stores AI response as 'assistant' message")
    
    print("\n🔄 State Flow:")
    print("1. user_input → messages (human)")
    print("2. messages → OpenAI API → ai_response")
    print("3. ai_response → messages (assistant)")
    print("4. is_complete = True")

if __name__ == "__main__":
    show_workflow_diagram()
