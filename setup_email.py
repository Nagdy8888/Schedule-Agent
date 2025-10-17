"""Email setup helper script."""
import os
from dotenv import load_dotenv

def check_email_setup():
    """Check which email method is configured."""
    load_dotenv()
    
    print("📧 Email Setup Check")
    print("=" * 40)
    
    # Check OAuth credentials
    oauth_creds = os.path.exists("credentials.json")
    oauth_token = os.path.exists("token.json")
    
    # Check SMTP credentials
    smtp_email = os.getenv("GMAIL_EMAIL")
    smtp_password = os.getenv("GMAIL_APP_PASSWORD")
    
    print("OAuth Method (Gmail API):")
    print(f"  credentials.json: {'✅ Found' if oauth_creds else '❌ Missing'}")
    print(f"  token.json: {'✅ Found' if oauth_token else '❌ Missing'}")
    
    print("\nSMTP Method (App Password):")
    print(f"  GMAIL_EMAIL: {'✅ Set' if smtp_email else '❌ Not set'}")
    print(f"  GMAIL_APP_PASSWORD: {'✅ Set' if smtp_password else '❌ Not set'}")
    
    print("\nRecommendations:")
    
    if oauth_creds and oauth_token:
        print("✅ OAuth is ready to use")
        print("   Run: python main.py")
    elif smtp_email and smtp_password:
        print("✅ SMTP is ready to use")
        print("   Run: python main_smtp.py")
    else:
        print("❌ No email method configured")
        print("\nChoose one method:")
        print("1. OAuth (Gmail API) - Follow gmail_quick_setup.md")
        print("2. SMTP (App Password) - Follow smtp_setup.md")

def create_smtp_main():
    """Create a main file that uses SMTP instead of OAuth."""
    smtp_main_content = '''"""Main entry point using SMTP instead of Gmail API."""
from main import create_agent_graph, run_agent, interactive_chat
from nodes_smtp import send_smtp_message
from langgraph.graph import StateGraph, END
from state import AgentState
from nodes import add_user_message, generate_ai_response, add_ai_message, should_send_email
from config import validate_config
from memory import get_memory

def create_smtp_agent_graph():
    """Create the LangGraph agent workflow with SMTP."""
    print("🔧 Building LangGraph workflow with SMTP...")
    
    # Initialize the graph with our state
    workflow = StateGraph(AgentState)
    
    # Add nodes to the graph
    workflow.add_node("add_user_message", add_user_message)
    workflow.add_node("generate_ai_response", generate_ai_response)
    workflow.add_node("add_ai_message", add_ai_message)
    workflow.add_node("send_smtp_message", send_smtp_message)
    
    # Set the entry point
    workflow.set_entry_point("add_user_message")
    
    # Connect the nodes with conditional routing
    workflow.add_edge("add_user_message", "generate_ai_response")
    workflow.add_edge("generate_ai_response", "add_ai_message")
    
    # Add conditional edge for email sending
    workflow.add_conditional_edges(
        "add_ai_message",
        should_send_email,
        {
            True: "send_smtp_message",
            False: END
        }
    )
    
    workflow.add_edge("send_smtp_message", END)
    
    # Compile the graph
    app = workflow.compile()
    
    print("✅ LangGraph workflow with SMTP created successfully!")
    return app

if __name__ == "__main__":
    # Replace the create_agent_graph function
    import main
    main.create_agent_graph = create_smtp_agent_graph
    
    # Run the main function
    main.interactive_chat()
'''
    
    with open("main_smtp.py", "w") as f:
        f.write(smtp_main_content)
    
    print("✅ Created main_smtp.py - Use this for SMTP method")

if __name__ == "__main__":
    check_email_setup()
    
    if input("\nCreate SMTP version? (y/N): ").lower() == 'y':
        create_smtp_main()
