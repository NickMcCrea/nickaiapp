import os
import openai
from  dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("AZURE_KEY")
openai.api_type = "azure"
openai.api_base = "https://armstale-aml-aoai.openai.azure.com"
openai.api_version = "2023-07-01-preview"

message_text = [{"role": "system", "content": "You are a helpful assistant."}]
message_text.append({"role": "user", "content": "Hi there! What's the best food to get from the bakery in Co-Op?"})


completion = openai.ChatCompletion.create(
    engine="gpt35turbo",
    messages=message_text,
    temperature=0.7,
    max_tokens=500,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
    )

response = completion['choices'][0]['message']['content']

print(response)
