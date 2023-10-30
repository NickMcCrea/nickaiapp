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
         "name": "get_data_sources",
            "description": f"""Use this function to answer user questions about what data sources we have available.
                            For example, the user may ask about data sources, or ask about a specific data source, table or column. 
                            """,
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
            }
        },
         {
         "name": "fall_back_function",
            "description": "Use this function to reply to user questions that don't match any of the other specified functions",
             "parameters": { "type": "object", "properties": {}}

        }

        ]

        self.function_mapping = {
            "get_data_sources": self.get_data_sources,
            "fall_back_function": self.fall_back_function
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
        
    