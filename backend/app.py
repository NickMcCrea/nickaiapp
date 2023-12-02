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

meta_data_service = MetaDataService()
meta_data_service.initialize_data_sources()

actions_manager = ActionsManager(current_model, meta_data_service)


# Costs for different models


#app route for getting meta data for a specific data source
@app.route("/get_meta_data", methods=["GET"])
def get_meta_data():
    user_session_state = get_user_session_state()
    session_id = session.get("session_id")
    
    #get the data source name from the query parameter
    data_source_name = request.args.get("data_source_name")

    data_source = meta_data_service.get_data_source(data_source_name)
    if data_source is None:
        return jsonify({"error": f"Data source {data_source_name} not found"}), 404
    
    meta_data = data_source['meta']
    return jsonify(meta_data), 200


@app.route("/ask_specific", methods=["POST"])
def ask_specific():
    user_session_state = get_user_session_state()
    session_id = session.get("session_id")
    user_input = request.json.get("input", "")
    data_source_name = request.json.get("data_source_name", "")
    user_session_state.set_specific_data_set(data_source_name)

    try:
        state = get_server_state(user_session_state)
        return state.process_request(socketio, session_id, actions_manager, user_session_state, user_input)
                    

    except Exception as e:
        print("Exception: ", e)
        return jsonify({"error": str(e)}), 500


@app.route("/ask", methods=["POST"])
def ask():
 
    # get session ID from the session object
    user_session_state = get_user_session_state()
    session_id = session.get("session_id")
    user_input = request.json.get("input", "")

    if user_session_state.get_specific_data_set() is not None:
        #set it to none
        user_session_state.set_specific_data_set(None)
   

    try:
        state = get_server_state(user_session_state)
        return state.process_request(socketio, session_id, actions_manager, user_session_state, user_input)
                    

    except Exception as e:
        print("Exception: ", e)
        return jsonify({"error": str(e)}), 500

def get_server_state(user_session_state: UserSessionState):
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
    socketio.run(app, debug=True, port=5001)

