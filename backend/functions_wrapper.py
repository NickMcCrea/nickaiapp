import json
import openai
import prompt_templates
import json

#constructor for a functions class
class FunctionsWrapper:

    def load_json(self,file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    #constructor
    def __init__(self, current_model):
        self.current_model = current_model
      
        
        self.top_songs = self.load_json("datasources/top_songs.json")
   


        self.functions = [      
        {
         "name": "query_available_data_sources",
            "description": f"""Use this function to answer user questions about what data sources we have available.
                            For example, the user may ask about data sources, or ask about a specific data source, or attribute. 
                            """,
          "parameters": {
                "type": "object",
                "properties": {}
            }
        },
         {
         "name": "fall_back_function",
            "description": "Use this function to reply to user questions that don't match any of the other specified functions",
             "parameters": { "type": "object", "properties": {}}

        }

        ]

        self.function_mapping = {
            "query_available_data_sources": self.get_data_sources,
            "fall_back_function": self.fall_back_function
            # Add more function mappings here...
        }
    
    def get_data_sources(self, user_input):

        prompt = f"""
                Given the following data source schemas:
                {self.top_songs}
              

                please answer the following questions succinctly:
                {user_input}

                Return the answer in the following JSON format:
                First, a list of relevant data source names.
                Second, very brief commentary on the answer in a JSON parameter called "commentary".
                E.g.
                {{"data_source_names": ["balances", "counterparties"], "commentary": "Here's data sources relevant to your query."}}

                or e.g.
                {{"data_source_names": ["balances", "counterparties", "products"], "commentary": "Here's all our data sources."}}

                Return only JSON. No other commentary outside of the JSON.
                """

        #print the user input we're using to generate a response
        print(f"User input: {user_input}")
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        messages.append({"role": "system", "content": "You are helping the user explore data sets, and answer questions about them."}) 
        messages.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model=self.current_model,
            messages=messages
        )
        output = response['choices'][0]['message']['content']
        return output

    def fall_back_function(self, user_input):
        return "I'm sorry, I don't understand."
        
    #getter
    def get_functions(self):
        return self.functions
    
   
    

    
    def execute_function(self, response_message, user_input, name, args):
 
        #print the function name and arguments
        print(f"Executing function '{name}' with arguments {args}")
        if name in self.function_mapping:
            func = self.function_mapping[name]
            return func(user_input, **args)
        else:
            raise ValueError(f"Function '{name}' not found.")
        
    