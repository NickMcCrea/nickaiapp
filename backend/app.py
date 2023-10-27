import os
import openai
from flask import Flask, request, jsonify,session
from dotenv import load_dotenv
from flask_cors import CORS
from uuid import uuid4
from ConversationHistory import ConversationHistory
import json
from functions import Functions


load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)
openai.api_key = os.getenv("OPENAI_KEY")
app.secret_key = os.getenv("SECRET_KEY")

gpt_3 = "gpt-3.5-turbo-0613"
gpt_4 = "gpt-4-0613"
current_model = gpt_3
user_sessions = {}
functions = Functions()



# Costs for different models
COSTS = {
    "gpt-3.5-turbo-0613": {"input": 0.0015 / 1000, "output": 0.002 / 1000},
    "gpt-4-0613": {"input": 0.03 / 1000, "output": 0.006 / 1000}
}

def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)


@app.route('/ask', methods=['POST'])
def ask():

    #get session ID from the session object
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
            functions=functions.get_functions(),
            function_call="auto"
        )

        #function call test
        response_message = response["choices"][0]["message"]
        function_response = None
        was_function_call = response_message.get("function_call")
        if was_function_call:
            #print 
            print("function call: ", response_message.get("function_call"))
            available_functions = {
            "get_current_weather": get_current_weather,
             }  # only one function in this example, but you can have multiple
            function_name = response_message["function_call"]["name"]
            function_to_call = available_functions[function_name]
            function_args = json.loads(response_message["function_call"]["arguments"])
            function_response = function_to_call(
                location=function_args.get("location"),
                unit=function_args.get("unit"),
            )



        assistant_output = response['choices'][0]['message']['content']
        conversation_history.add_assistant_message(assistant_output)  # Add assistant output to history


        tokens_used = response['usage']['total_tokens']
        input_tokens = response['usage']['prompt_tokens']
        output_tokens = tokens_used - input_tokens

        # Calculate estimated cost
        input_cost = COSTS[current_model]['input'] * input_tokens
        output_cost = COSTS[current_model]['output'] * output_tokens
        estimated_cost = input_cost + output_cost
        
        cost_so_far = conversation_history.get_total_estimated_cost()
        conversation_history.set_total_estimated_cost(cost_so_far + estimated_cost)

        print("Total estimated cost: {:.10f}".format(conversation_history.get_total_estimated_cost()))

        return jsonify({'function_response': function_response, 'function_call':  was_function_call, 'output': assistant_output, 'estimated_cost': "{:.10f}".format(conversation_history.get_total_estimated_cost())}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)