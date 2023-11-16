import os
import openai
from flask import Flask, request, jsonify,session
from dotenv import load_dotenv
from flask_cors import CORS
from uuid import uuid4
import json
from openaihelpers.actions import ActionsManager
import time
from flask_socketio import SocketIO, emit, join_room, leave_room
from typing import Dict, List, Any
from conversation_history import ConversationHistory



load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)
openai.api_key = os.getenv("OPENAI_KEY")
app.secret_key = os.getenv("SECRET_KEY")


# After your Flask app initialization
socketio = SocketIO(app, cors_allowed_origins="*")

gpt_3 = "gpt-3.5-turbo-0613"
#gpt_4 = "gpt-4-0613"
gpt_4 = "gpt-4-1106-preview"
current_model = gpt_4
user_sessions = {}

@socketio.on('connect')
def on_connect():
    # Access the session_id from the Flask session
    session_id = session.get('session_id', str(uuid4()))
    # Save the session_id back to the session to persist it
    session['session_id'] = session_id
    # Join the room with the session_id
    join_room(session_id)
    emit('connected', {'message': 'Connected to WebSocket', 'session_id': session_id})


@socketio.on('disconnect')
def on_disconnect():
    session_id = session.get('session_id')
    if session_id:
        leave_room(session_id)
        # Perform additional cleanup if needed, e.g., removing session from user_sessions dict
        user_sessions.pop(session_id, None)
        print(f"Session {session_id} has disconnected.")



actions_manager = ActionsManager(current_model)

    



# Costs for different models
COSTS = {
    "gpt-3.5-turbo-0613": {"input": 0.0015 / 1000, "output": 0.002 / 1000},
    "gpt-4-0613": {"input": 0.03 / 1000, "output": 0.006 / 1000},
    "gpt-4-1106-preview": {"input": 0.01 / 1000, "output": 0.003 / 1000}
}

def dummy_function():
    return "dummy function"



@app.route('/ask', methods=['POST'])
def ask():

    #start the timer
    start_time = time.time()

    #get session ID from the session object
    conversation_history = get_convo_history()
    session_id = session.get('session_id')
    user_input = request.json.get('input', '')

    #log the model property from the request
    model = request.json.get('model', '')
    print("model: ", model)

    #set current_model based on what we got from the client
    global current_model
    if model == "GPT3.5":
        current_model = gpt_3
        print("current_model: ", current_model)
    elif model == "GPT4":
        current_model = gpt_4
        print("current_model: ", current_model)


    try:

        # Add user message to conversation history
        conversation_history.add_user_message(user_input)

        

        response = openai.ChatCompletion.create(
            model=current_model,
            messages=conversation_history.get_messages(),
            functions=actions_manager.get_functions(),
            function_call="auto"
        )

        #print the time up til now
        print("Time elapsed 1: ", time.time() - start_time)
       
        response_message = response["choices"][0]["message"]
        print("response_message: ", response_message)
        
        function_response = None
        was_function_call = response_message.get("function_call")

        chat_output = None
        data = None
        metadata = None

        if was_function_call:
            data, metadata, commentary = get_function_response(socketio, session_id, conversation_history, response_message, user_input)
  
        else:
            commentary = response['choices'][0]['message']['content']

        #print the time up til now
        print("Time elapsed 2: ", time.time() - start_time)
       
        if chat_output is None:
           chat_output = ""

        conversation_history.add_assistant_message(commentary)  # Add assistant output to history

        

        #if data and metadata are None,
        #set the chat output to "Sorry, I didn't understand - can you rephrase that?"
        if data is None and metadata is None and commentary == '':
            commentary = "Sorry, I didn't understand - can you rephrase that?"

      
        #print the time up til now
        print("Time elapsed 3: ", time.time() - start_time)


        final_response = jsonify({'function_response': function_response, 'function_call':  was_function_call, 'output': commentary, 'data': data, 'metadata': metadata})
        print("final_response: ", final_response)
        return final_response, 200

    except Exception as e:
        print("Exception: ", e)
        return jsonify({'error': str(e)}), 500

def get_convo_history() -> ConversationHistory:
    session_id = session.get('session_id')

    #check if the user_sessions dictionary has a key for the current session ID
    if session_id not in user_sessions:
        #print that we're creating a new session ID
        print("Creating new convo history...")
        user_sessions[session_id] = ConversationHistory()

    #get the conversation history for the current session ID
    conversation_history = user_sessions.get(session_id)

    #print session ID
    print("session_id: ", session_id)
    return conversation_history

def get_function_response(socket_io: SocketIO, session_id: str,conversation_history: ConversationHistory, response_message: Dict[str,Any], user_input: str):
    function_name = response_message["function_call"]["name"]
    function_args = json.loads(response_message["function_call"]["arguments"])

    #emit a progress event to the client
    progress_data = {'status': function_name, 'message': 'function called'}
    socketio.emit('progress', progress_data, room=session_id)

    data,metadata,commentary = actions_manager.execute_function(socketio, session_id, conversation_history, response_message, user_input, function_name, function_args)
    return data,metadata, commentary


if __name__ == '__main__':
    app.run(debug=True, port=5001)