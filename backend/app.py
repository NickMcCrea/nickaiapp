import os
import openai
from flask import Flask, request, jsonify,session
from dotenv import load_dotenv
from flask_cors import CORS
from uuid import uuid4
from ConversationHistory import ConversationHistory
import json
from functions_wrapper import FunctionsWrapper
import prompt_templates as prompt_templates
from datasources.data_source_loader import DataSourceLoader


load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)
openai.api_key = os.getenv("OPENAI_KEY")
app.secret_key = os.getenv("SECRET_KEY")

gpt_3 = "gpt-3.5-turbo-0613"
gpt_4 = "gpt-4-0613"
current_model = gpt_4
user_sessions = {}

data_source_loader = DataSourceLoader()
data_source_loader.load_from_file("datasources/nicktrialbalance.json")


# print each data source
for data_source_name, data_source_obj in data_source_loader.data_sources.items():
    print(f"data_source name: {data_source_name}")
    print(f"data_source details: {data_source_obj}")

functions = FunctionsWrapper(current_model, data_source_loader)

    



# Costs for different models
COSTS = {
    "gpt-3.5-turbo-0613": {"input": 0.0015 / 1000, "output": 0.002 / 1000},
    "gpt-4-0613": {"input": 0.03 / 1000, "output": 0.006 / 1000}
}

def dummy_function():
    return "dummy function"



@app.route('/ask', methods=['POST'])
def ask():

    #get session ID from the session object
    conversation_history = get_convo_history()

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

       
        response_message = response["choices"][0]["message"]
        
        function_response = None
        was_function_call = response_message.get("function_call")

        if was_function_call:
            function_response = get_function_response(response_message, user_input)


        chat_output = response['choices'][0]['message']['content']
        if chat_output is None:
            chat_output = ""

        conversation_history.add_assistant_message(chat_output)  # Add assistant output to history


        input_tokens, output_tokens = calculate_tokens(response)

        # Calculate estimated cost
        estimated_cost = calculate_costs(input_tokens, output_tokens)     
        cost_so_far = conversation_history.get_total_estimated_cost()
        conversation_history.set_total_estimated_cost(cost_so_far + estimated_cost)

        print("Total estimated cost: {:.10f}".format(conversation_history.get_total_estimated_cost()))

        return jsonify({'function_response': function_response, 'function_call':  was_function_call, 'output': chat_output, 'estimated_cost': "{:.10f}".format(conversation_history.get_total_estimated_cost())}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_convo_history():
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

def get_function_response(response_message, user_input):
    function_name = response_message["function_call"]["name"]
    #print("function_name: ", function_name)
    function_args = json.loads(response_message["function_call"]["arguments"])
    #print("function_args: ", function_args)
    function_response = functions.execute_function(response_message, user_input, function_name, function_args)
    return function_response

def calculate_costs(input_tokens, output_tokens):
    input_cost = COSTS[current_model]['input'] * input_tokens
    output_cost = COSTS[current_model]['output'] * output_tokens
    estimated_cost = input_cost + output_cost
    return estimated_cost

def calculate_tokens(response):
    tokens_used = response['usage']['total_tokens']
    input_tokens = response['usage']['prompt_tokens']
    output_tokens = tokens_used - input_tokens
    return input_tokens,output_tokens

if __name__ == '__main__':
    app.run(debug=True, port=5001)