import openai
from flask import jsonify
import json
from typing import Dict, List, Any
from flask_socketio import SocketIO
from user_session_state import UserSessionState
from actions import ActionsManager

class DefaultAppState:

    def process_request(self, socketio, session_id, actions_manager, user_session_state, user_input):

        user_session_state.add_user_message(user_input)

        

        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=user_session_state.get_messages(),
            functions=actions_manager.get_functions(),
            function_call="auto"
        )

        #print the time up til now
       
        response_message = response["choices"][0]["message"]
        print("response_message: ", response_message)
        
        function_response = None
        was_function_call = response_message.get("function_call")

        commentary = None
        data = None
        metadata = None

        if was_function_call:
            data, metadata, commentary = self.get_function_response(socketio, session_id, actions_manager, user_session_state, response_message, user_input)
  
        else:
            commentary = response['choices'][0]['message']['content']

    

        user_session_state.add_assistant_message(commentary)  # Add assistant output to history

        
        #if data and metadata are None,
        #set the chat output to "Sorry, I didn't understand - can you rephrase that?"
        if data is None and metadata is None and commentary == '':
            commentary = "Sorry, I didn't understand - can you rephrase that?"

      

        final_response = jsonify({'function_response': function_response, 'function_call':  was_function_call, 'output': commentary, 'data': data, 'metadata': metadata})
        print("final_response: ", final_response)
        return final_response, 200




    def get_function_response(self, socket_io: SocketIO, session_id: str, actions_manager: ActionsManager, conversation_history: UserSessionState, response_message: Dict[str,Any], user_input: str):
        function_name = response_message["function_call"]["name"]
        function_args = json.loads(response_message["function_call"]["arguments"])

        #emit a progress event to the client
        progress_data = {'status': function_name, 'message': 'function called'}
        socket_io.emit('progress', progress_data, room=session_id)

        data,metadata,commentary = actions_manager.execute_function(socket_io, session_id, conversation_history, response_message, user_input, function_name, function_args)
        return data,metadata, commentary
        