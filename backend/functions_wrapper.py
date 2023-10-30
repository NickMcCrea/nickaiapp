import json
import openai
import prompt_templates

#constructor for a functions class
class FunctionsWrapper:

    

    #constructor
    def __init__(self, current_model, data_source_loader):
        self.current_model = current_model
        self.data_source_loader = data_source_loader
        self.functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },


        },
        {
         "name": "get_data_sources",
            "description": "Use this function to answer user questions about what data sources we have available.",
          "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": f"""
                            The specific question the user asked, verbatim i.e. the query that prompted this function call."
                                """,
                    }
                },
                "required": ["query"],
            },
        }

        ]

        self.function_mapping = {
            "get_current_weather": self.get_current_weather,
            "get_data_sources": self.get_data_sources
            # Add more function mappings here...
        }
    
    def get_data_sources(self, user_input, query):

        #print the user input we're using to generate a response
        print(f"User input: {user_input}")
        messages = [{"role": "system", "content": "You are an expert at reading JSON and inferring the data sources it refers to."}] 
        messages.append({"role": "system", "content": "Ignore the connectivity details or the type of underlying data source (e.g. sqlite or csv)."})
        messages.append({"role": "user", "content": prompt_templates.generate_datasources_prompt(self.data_source_loader.get_data_source_string(), user_input)})
        response = openai.ChatCompletion.create(
            model=self.current_model,
            messages=messages
        )
        output = response['choices'][0]['message']['content']
        return output

        
    #getter
    def get_functions(self):
        return self.functions
    
    def get_current_weather(self, location, unit="fahrenheit"):
        """Get the current weather in a given location"""
        weather_info = {
            "location": location,
            "temperature": "72",
            "unit": unit,
            "forecast": ["sunny", "windy"],
        }
        return json.dumps(weather_info)
    

    
    def execute_function(self, response_message, user_input, name, args):
 
        #print the function name and arguments
        print(f"Executing function '{name}' with arguments {args}")
        if name in self.function_mapping:
            func = self.function_mapping[name]
            return func(user_input, **args)
        else:
            raise ValueError(f"Function '{name}' not found.")
        
    