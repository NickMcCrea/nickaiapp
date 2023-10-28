import json

#constructor for a functions class
class FunctionsWrapper:

    #constructor
    def __init__(self):
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

        
        ]

        self.function_mapping = {
            "get_current_weather": self.get_current_weather
            # Add more function mappings here...
        }
    
        
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
    

    
    def execute_function(self, name, args):
 
        #print the function name and arguments
        print(f"Executing function '{name}' with arguments {args}")
        if name in self.function_mapping:
            func = self.function_mapping[name]
            return func(**args)
        else:
            raise ValueError(f"Function '{name}' not found.")
        
    