"""Simple Flask web UI for testing the AI agent."""
from flask import Flask, render_template, request, jsonify, Response
import json
from datetime import datetime
from main import run_agent
import time

app = Flask(__name__)

@app.route('/')
def index():
    """Main page with chat interface."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the web UI."""
    try:
        data = request.get_json()
        user_input = data.get('message', '').strip()
        
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400
        
        # Run the agent with the user input (silent mode for web UI)
        result = run_agent(user_input, silent=True)
        
        # Extract the AI response
        ai_response = result.get('ai_response', 'No response generated')
        
        # Extract email status
        email_sent = result.get('email_sent', False)
        email_content = result.get('email_content', '')
        
        # Extract weather status
        weather_summary = result.get('weather_summary', '')
        
        # Extract memory info
        total_messages = len(result.get('messages', []))
        
        # Format the response
        response_data = {
            'ai_response': ai_response,
            'email_sent': email_sent,
            'email_content': email_content,
            'weather_summary': weather_summary,
            'total_messages': total_messages,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': f'Error processing request: {str(e)}'}), 500

@app.route('/chat/stream', methods=['POST'])
def chat_stream():
    """Handle streaming chat messages from the web UI."""
    try:
        # Get the request data and run agent outside the generator
        data = request.get_json()
        user_input = data.get('message', '').strip()
        
        if not user_input:
            return Response(f"data: {json.dumps({'error': 'No message provided'})}\n\n", mimetype='text/plain')
        
        # Run the agent with the user input (silent mode for web UI)
        result = run_agent(user_input, silent=True)
        
        # Extract the AI response
        ai_response = result.get('ai_response', 'No response generated')
        
        # Extract other status information
        email_sent = result.get('email_sent', False)
        email_content = result.get('email_content', '')
        weather_summary = result.get('weather_summary', '')
        total_messages = len(result.get('messages', []))
        
        def generate():
            try:
                # Stream the AI response word by word
                words = ai_response.split()
                current_text = ""
                
                for i, word in enumerate(words):
                    current_text += word + " "
                    
                    # Send partial response
                    partial_data = {
                        'type': 'partial',
                        'content': current_text.strip(),
                        'is_complete': False
                    }
                    yield f"data: {json.dumps(partial_data)}\n\n"
                    
                    # Add a small delay to simulate typing
                    time.sleep(0.05)
                
                # Send final response with all status information
                final_data = {
                    'type': 'complete',
                    'ai_response': ai_response,
                    'email_sent': email_sent,
                    'email_content': email_content,
                    'weather_summary': weather_summary,
                    'total_messages': total_messages,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'is_complete': True
                }
                yield f"data: {json.dumps(final_data)}\n\n"
                
            except Exception as e:
                error_data = {
                    'type': 'error',
                    'error': f'Error in streaming: {str(e)}',
                    'is_complete': True
                }
                yield f"data: {json.dumps(error_data)}\n\n"
        
        return Response(generate(), mimetype='text/plain')
        
    except Exception as e:
        error_data = {
            'type': 'error',
            'error': f'Error processing request: {str(e)}',
            'is_complete': True
        }
        return Response(f"data: {json.dumps(error_data)}\n\n", mimetype='text/plain')

@app.route('/clear', methods=['POST'])
def clear_chat():
    """Clear chat memory."""
    try:
        # Clear the chat memory file
        with open('chat_memory.json', 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        
        return jsonify({'success': True, 'message': 'Chat memory cleared'})
        
    except Exception as e:
        return jsonify({'error': f'Error clearing memory: {str(e)}'}), 500

if __name__ == '__main__':
    print("Starting Flask web UI...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
