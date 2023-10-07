import os
import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from ConversationHistory import ConversationHistory

load_dotenv()

app = Flask(__name__)
CORS(app)
openai.api_key = os.getenv("OPENAI_KEY")

gpt_3 = "gpt-3.5-turbo"
gpt_4 = "gpt-4"
current_model = gpt_3
conversation_history = ConversationHistory()




# Costs for different models
COSTS = {
    "gpt-3.5-turbo": {"input": 0.0015 / 1000, "output": 0.002 / 1000},
    "gpt-4": {"input": 0.03 / 1000, "output": 0.006 / 1000}
}

#a route to switch between the models used in the backend
@app.route('/model', methods=['POST'])
def model():
    global current_mdoel
    model = request.json.get('model', '')
    if model == "GPT3":
        current_model = gpt_3
        return jsonify({'model': current_model}), 200
    if model == "GPT4":
        current_model = gpt_4
        return jsonify({'model': current_model}), 200
    else:
        return jsonify({'error': 'Model not found'}), 500




@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('input', '')
   

    try:

        # Add user message to conversation history
        conversation_history.add_user_message(user_input)

        response = openai.ChatCompletion.create(
            model=current_model,
            messages=conversation_history.get_messages()
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

        return jsonify({'output': assistant_output, 'estimated_cost': "{:.10f}".format(conversation_history.get_total_estimated_cost())}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)