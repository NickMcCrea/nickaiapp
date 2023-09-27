import os
import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_KEY")
gpt_3 = "gpt-3.5-turbo"
gpt_4 = "gpt-4"

# Costs for different models
COSTS = {
    "gpt-3.5-turbo": {"input": 0.0015 / 1000, "output": 0.002 / 1000},
    "gpt-4": {"input": 0.03 / 1000, "output": 0.006 / 1000}
}

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('input', '')
    model = gpt_3

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ]
        )

        assistant_output = response['choices'][0]['message']['content']
        tokens_used = response['usage']['total_tokens']
        input_tokens = response['usage']['prompt_tokens']
        output_tokens = tokens_used - input_tokens

        # Calculate estimated cost
        input_cost = COSTS[model]['input'] * input_tokens
        output_cost = COSTS[model]['output'] * output_tokens
        estimated_cost = input_cost + output_cost

        return jsonify({'output': assistant_output, 'estimated_cost': estimated_cost}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)