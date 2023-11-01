import json
import openai
import prompt_templates
import json
from in_memory_db import InMemoryDB
from MetaDataService import MetaDataService

#constructor for a functions class
class FunctionsWrapper:



    #constructor
    def __init__(self, current_model):
        self.current_model = current_model


        self.data_service = MetaDataService()

           # Example usage
#repository = DataRepository()
#restaurant_info = repository.get_data_source('restaurant_info')
#if restaurant_info:
#    meta = restaurant_info['meta']
#    db = restaurant_info['db']

        #add the names of the data sets meta data we have available to a dictionary

    


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
         "name": "query_data",
            "description": f"""Use this function when a user asks for a question that requires a data query.
                            If they want to see actual data, use this function. 
                            If we can infer the data source from the user's question, we should input that information. 
                            Users may ask for refined data from a previous query, e.g. "Can you filter that on restaurants with delivery times < 30 mins?"
                            """,
          "parameters": {
                "type": "object",
                "properties": 
                {
                    "data_source_name": {
                        "type": "string",
                        "description": "The name of the data source to fetch data from."
                           
                    }
                }
            }
        }
        ]

        self.function_mapping = {
            "query_available_data_sources": self.data_sourcing_general_query,
            "query_data": self.fetch_data_from_source
            # Add more function mappings here...
        }


    def fetch_data_from_source(self, convo_history, user_input, data_source_name):
        #if data source is not none
        commentary = ""

        data_source = self.data_service.get_data_source(data_source_name)

        if data_source is None:
            print(f"Data set unknown. Determining data source from user input '{user_input}'")
            data_source_json = self.determine_data_source(convo_history,user_input)
            data_source_name = data_source_json["data_source"]
            data_source = self.data_service.get_data_source(data_source_name)
            #print the data source name
            print(f"Data source name: {data_source_name}")
           
           
        response = self.get_data_query(convo_history, user_input,data_source["meta"])
        print(response)
        data = self.data_service.query(response["SQL"], data_source_name)
        
        return data, f"DataQuery: Data source name: {data_source_name}, Query: {response['SQL']}"

    
    def determine_data_source(self, convo_history, user_input):

        spotify_data_meta = self.data_service.get_data_source("spotify_track_data")["meta"]
        restaurants_data_meta = self.data_service.get_data_source("restaurant_info")["meta"]

        prompt = f"""
                Given the following data source schemas:
                {spotify_data_meta}
                {restaurants_data_meta}
                
                please determine the best single data source, to fetch data to answer the following questions succinctly:
                {user_input}

                Here's the conversation history so far, to help determine:
                {convo_history.messages}

                Return the answer in the following JSON format:
                {{"data_source": "data_source_name"}}
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
        return json.loads(output)

    #in a real system, this would be probably combine some embeddings search with a metadata service. 
    #we'll fake it for now. 
    def data_sourcing_general_query(self, convo_history, user_input):

        spotify_data_meta = self.data_service.get_data_source("spotify_track_data")["meta"]
        restaurants_data_meta = self.data_service.get_data_source("restaurant_info")["meta"]

        prompt = f"""
                Given the following data source schemas:
                {spotify_data_meta}
                {restaurants_data_meta}
                
                please answer the following questions succinctly:
                {user_input}

                if needed, here's the most recent convo messages so far, if it helps to give context:
                {convo_history.messages}
                
                
                
            
                Return the answer in the following JSON format:
                First, a list of relevant data source names.
                Second, very brief commentary on the answer in a JSON parameter called "commentary".
                E.g.
                {{"data_source_names": ["datasource1", "datasource2"], "commentary": "Here's data sources relevant to your query, they are relevant because..."}}

                or e.g.
                {{"data_source_names": ["datasource1", "datasource2", "datasource3"], "commentary": "Here's all our data sources."}}

                or e.g.
                {{"data_source_names": [], "commentary": "We don't have any data sources that match your query."}}

                or e.g.
                {{"data_source_names": ["datasource1", "commentary": "This is the only datasource available"}}

                where the user is clearly looking for data, and we can identify a data source, we should write a SQL query to extract the data.
                e.g.
                {{"data_source_names": ["datasource1"], "commentary": "Here's the data you're looking for.", "sql_query": "SELECT * FROM datasource1 WHERE ..."}}

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
        commentary = response['choices'][0]['message']['content']
        return "", commentary


    def get_data_query(self, convo_history, user_input, data_source_meta):

        prompt = f"""
                Given the following data source schemas:
                {data_source_meta}

                And the previous conversation history:
                {convo_history.messages}
                
                please generate JSON to help generate data, to the following questions succinctly:
                {user_input}

                Return the answer in the following JSON format:
                E.g.
                {{"SQL": "select * from data_source_name where ..."}}

                Return only JSON. No other commentary outside of the JSON.
                """

        #print the user input we're using to generate a response
        print(f"User input: {user_input}")
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        messages.append({"role": "system", "content": "You are helping the user explore data sets, and generate valid SQL queries to questions about them."}) 
        messages.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model=self.current_model,
            messages=messages
        )
        output = response['choices'][0]['message']['content']
        return json.loads(output)


     
    #getter
    def get_functions(self):
        return self.functions
    
   
    

    
    def execute_function(self, convo_history,  response_message, user_input, name, args):
 
        #print the function name and arguments
        print(f"Executing function '{name}' with arguments {args}")
        if name in self.function_mapping:
            func = self.function_mapping[name]
            data, commentary = func(convo_history, user_input, **args)
            return data, commentary
        else:
            raise ValueError(f"Function '{name}' not found.")
        
    