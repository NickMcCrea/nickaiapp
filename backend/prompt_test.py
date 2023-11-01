import requests
import openai
from dotenv import load_dotenv
import os
import time
import json


load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")

gpt_3 = "gpt-3.5-turbo-0613"
gpt_4 = "gpt-4-0613"
current_model = gpt_4

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

query = "what data sets do we have that contain GICS codes?"




messages = [{"role": "system", "content": "You are a helpful assistant."}]
messages.append({"role": "system", "content": "You are helping the user explore data sets, and answer questions about them."})
messages.append({"role": "user", "content": query})

balances = load_json("datasources/balances.json")
counterparties = load_json("datasources/counterparties.json")
products = load_json("datasources/products.json")


prompt = f"""
        Given the following data source schemas:
        {balances}
        {counterparties}
        {products}

        please answer the following questions succinctly:
        {query}

        Return the answer in the following JSON format:
        First, a list of relevant data source names.
        Second, commentary on the answer in a JSON parameter called "commentary".

        E.g.
        {{"data_source_names": ["balances", "counterparties"], "commentary": "The user is asking about balances and counterparties."}}

        Return only JSON. No other commentary outside of the JSON.
        """

#start timer
start_time = time.time()



messages = [{"role": "system", "content": "You are a helpful assistant."}]
messages.append({"role": "system", "content": "You are helping the user explore data sets, and answer questions about them."})
messages.append({"role": "user", "content": prompt})

response2 = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )


#end timer
print("Time elapsed: ", time.time() - start_time)
#print response
print(response2)





