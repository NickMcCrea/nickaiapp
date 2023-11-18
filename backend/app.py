import os
import openai
from flask import Flask, request, jsonify, session
from dotenv import load_dotenv
from flask_cors import CORS
from uuid import uuid4
import json
from actions import ActionsManager
import time
from flask_socketio import SocketIO, emit, join_room, leave_room
from typing import Dict, List, Any
from app_state import DefaultAppState
from meta_data_service import MetaDataService
from user_session_state import UserSessionState


load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)
openai.api_key = os.getenv("OPENAI_KEY")
app.secret_key = os.getenv("SECRET_KEY")

app_state_default = DefaultAppState()


# After your Flask app initialization
socketio = SocketIO(app, cors_allowed_origins="*")
current_model = "gpt-4-1106-preview"
user_sessions = {}


@socketio.on("connect")
def on_connect():
    # Access the session_id from the Flask session
    session_id = session.get("session_id", str(uuid4()))
    # Save the session_id back to the session to persist it
    session["session_id"] = session_id
    # Join the room with the session_id
    join_room(session_id)
    emit("connected", {"message": "Connected to WebSocket", "session_id": session_id})

@socketio.on("disconnect")
def on_disconnect():
    session_id = session.get("session_id")
    if session_id:
        leave_room(session_id)
        # Perform additional cleanup if needed, e.g., removing session from user_sessions dict
        user_sessions.pop(session_id, None)
        print(f"Session {session_id} has disconnected.")


actions_manager = ActionsManager(current_model, MetaDataService())


# Costs for different models
COSTS = {
    "gpt-3.5-turbo-0613": {"input": 0.0015 / 1000, "output": 0.002 / 1000},
    "gpt-4-0613": {"input": 0.03 / 1000, "output": 0.006 / 1000},
    "gpt-4-1106-preview": {"input": 0.01 / 1000, "output": 0.003 / 1000},
}



@app.route("/ask", methods=["POST"])
def ask():
 
    # get session ID from the session object
    user_session_state = get_user_session_state()
    session_id = session.get("session_id")
    user_input = request.json.get("input", "")

    try:
        state = get_server_state(user_session_state)
        return state.process_request(socketio, session_id, actions_manager, user_session_state, user_input)
                    

    except Exception as e:
        print("Exception: ", e)
        return jsonify({"error": str(e)}), 500

def get_server_state(user_session_state: UserSessionState):
    if user_session_state.get_app_state() == "Default" or user_session_state.get_app_state() == "Workspace":
        return app_state_default
    
   

def get_user_session_state() -> UserSessionState:
    session_id = session.get("session_id")

    # check if the user_sessions dictionary has a key for the current session ID
    if session_id not in user_sessions:
        # print that we're creating a new session ID
        print("Creating new convo history...")
        user_sessions[session_id] = UserSessionState()

    # get the conversation history for the current session ID
    conversation_history = user_sessions.get(session_id)

    # print session ID
    print("session_id: ", session_id)
    return conversation_history


if __name__ == "__main__":
    app.run(debug=True, port=5001)
