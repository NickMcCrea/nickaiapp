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


        self.functions = [      
        {
         "name": "query_meta_data",
            "description": f"""Use this function to answer user questions about what data sources we have available.
                            For example, the user may ask about data sources, or ask about a specific data source, or attribute. 
                            """,
          "parameters": {
                "type": "object",
                "properties": {}
            }
        },
         {
         "name": "fetch_meta_data",
            "description": f"""Use this function to retrieve meta data about a data source.
                            Use this when the user asks to see meta data or schema information about a data source. 
                            """,
          "parameters": {
                "type": "object",
                "properties": 
                {
                    "data_source_name": {
                        "type": "string",
                        "description": "The name of the meta data source to fetch data from."
                           
                    },
                     "ai_commentary": {
                        "type": "string",
                        "description": "Any comment from the assistant, on the request"
                           
                    }
                }
            }
        },

         {
         "name": "fetch_data",
            "description": f"""Use this function when a user asks for a question that requires a data query.
                            If they want to see actual data, use this function. 
                            If we can infer the data source from the context, we should input that information. 
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


        },
         {
         "name": "fetch_bar_chart_data",
            "description": f"""Use this function when a user asks for a question that requires a bar chart or bar graph.
                            If we can infer the data source from the context, we should input that information. 
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
         }, 
         {
         "name": "fetch_line_chart_data",
            "description": f"""Use this function when a user asks for a question that requires a line chart or time series.
                            If we can infer the data source from the context, we should input that information. 
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
            "query_meta_data": self.function_query_meta_data,
            "fetch_data": self.function_fetch_data,
            "fetch_meta_data": self.function_fetch_meta_data,
            "fetch_bar_chart_data": self.function_fetch_bar_chart_data,
            "fetch_line_chart_data": self.function_fetch_line_chart_data    
            # Add more function mappings here...
        }

    #in a real system, this would be probably combine some embeddings search with a metadata service. 
    #we'll fake it for now. 
    def function_query_meta_data(self, socketio, session_id, convo_history, user_input):

        

        prompt = f"""
                Given the following data source schemas:
                {self.data_service.get_all_meta_data()}
                
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
        data = None
        metadata= None
        return data, metadata, commentary

    #fetch actual data. fires off an open ai call to infer data source if we didn't infer in the function call
    def function_fetch_data(self, socketio, session_id, convo_history, user_input, data_source_name):
        #if data source is not none
        commentary = ""
        data_source = self.data_service.get_data_source(data_source_name)
        if data_source is None:
            data_source_name, data_source = self.open_ai_infer_data_source(socketio, session_id, convo_history, user_input)
           
           
        response = self.open_ai_generate_sql(socketio, session_id, convo_history, user_input,data_source["meta"], self.table_sql_prompt(convo_history, user_input, data_source["meta"]))

        print(response)
        data = self.data_service.query(response["SQL"], data_source_name)
        metadata = None
        commentary = f"DataQuery: Data source name: {data_source_name}, Query: {response['SQL']}"
        return data, metadata, commentary
    
    def function_fetch_bar_chart_data(self, socketio, session_id, convo_history, user_input, data_source_name):
        #if data source is not none
        commentary = ""
        data_source = self.data_service.get_data_source(data_source_name)
        if data_source is None:
            data_source_name, data_source = self.open_ai_infer_data_source(socketio, session_id, convo_history, user_input)
           
           
        response = self.open_ai_generate_sql(socketio, session_id, convo_history, user_input,data_source["meta"], self.bar_graph_sql_prompt(convo_history, user_input, data_source["meta"]))
        print(response)
        data = self.data_service.query(response["SQL"], data_source_name)
        metadata = None
        commentary = f"DataQuery: Data source name: {data_source_name}, Query: {response['SQL']}"
        return data, metadata, commentary
    
    def function_fetch_line_chart_data(self, socketio, session_id, convo_history, user_input, data_source_name):
        #if data source is not none
        commentary = ""
        data_source = self.data_service.get_data_source(data_source_name)
        if data_source is None:
            data_source_name, data_source = self.open_ai_infer_data_source(socketio, session_id, convo_history, user_input)
           
           
        response = self.open_ai_generate_sql(socketio, session_id, convo_history, user_input,data_source["meta"], self.line_graph_sql_prompt(convo_history, user_input, data_source["meta"]))
        
        print(response)
        data = self.data_service.query(response["SQL"], data_source_name)
        metadata = None
        commentary = f"DataQuery: Data source name: {data_source_name}, Query: {response['SQL']}"
        return data, metadata, commentary
    

    def function_fetch_meta_data(self, socketio, session_id, convo_history, user_input, data_source_name=None, ai_commentary=None):
        data_source = self.data_service.get_data_source(data_source_name)
        if data_source is None:
            data_source_name, data_source = self.open_ai_infer_data_source(socketio, session_id, convo_history, user_input)

        data = None
        metadata = self.data_service.get_data_source(data_source_name)["meta"]
       

        return data, metadata, f"Here's the meta data for {data_source_name}"

    def open_ai_infer_data_source(self, socketio, session_id, convo_history, user_input):
        print(f"Data set unknown. Determining data source from user input '{user_input}'")

        progress_data = {'status': 'data_source_inference', 'message': 'Inferring Data Source'}
        socketio.emit('progress', progress_data, room=session_id)

        prompt = f"""
                Given the following data source schemas:
                {self.data_service.get_all_meta_data()} 
                
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
        data_source_json = json.loads(output)

        data_source_name = data_source_json["data_source"]
        data_source = self.data_service.get_data_source(data_source_name)
            #print the data source name
        print(f"Data source name: {data_source_name}")

        
        return data_source_name, data_source

    def open_ai_generate_sql(self, socketio, session_id, convo_history, user_input, data_source_meta, prompt):

        progress_data = {'status': 'data_query_generation', 'message': 'Generating Data Query'}
        socketio.emit('progress', progress_data, room=session_id)

        #get the data source name
        data_source_name = data_source_meta["name"]

        prompt_additions = f"""
        The user may use shorthand for values (e.g. IS for Insitutional Securities), make sure to refer to 
        the data source schema for the full list of values. Always use the proper values, i.e. Institution Securities, not IS.
        Permitted values for each column are as follows:
        category - 'Revenues', 'Underwriting', 'Non Interest Expenses', 'Provision for Credit Losses'
        segment - 'Institutional Securities', 'Wealth Management', 'Investment Management'
        quarter - the format is YYYYQ1, YYYYQ2, YYYYQ3, YYYYQ4 etc. 
        """
     
        #if data source name is "financial_results", add on the prompt additions
        if data_source_name == "financial_results":
            print("Financial results data source detected. Adding prompt additions.")
            prompt += prompt_additions

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

    def table_sql_prompt(self, convo_history, user_input, data_source_meta):
        prompt = f"""
                Given the following data source schema:
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
                
        return prompt 
    
    def bar_graph_sql_prompt(self, convo_history, user_input, data_source_meta):
        prompt = f"""
                Given the following data source schema:
                {data_source_meta}
                And the previous conversation history:
                {convo_history.messages}
                please generate JSON to help generate data, to the following questions succinctly:
                {user_input}
                Return the answer in the following JSON format:
                E.g.
                {{"SQL": "select * from data_source_name where ..."}}
                Return only JSON. No other commentary outside of the JSON.
                Generated SQL queries should be bar chart-friendly.
                Whatever column is selected as the x-axis name as "X-Axis".
                Whatever column is selected as the y-axis should be a number - rename it as "Total". 
                """
                
        return prompt 
    
    def line_graph_sql_prompt(self, convo_history, user_input, data_source_meta):
        prompt = f"""
                Given the following data source schema:
                {data_source_meta}
                And the previous conversation history:
                {convo_history.messages}
                please generate JSON to help generate data, to the following questions succinctly:
                {user_input}
                Return the answer in the following JSON format:
                E.g.
                {{"SQL": "select * from data_source_name where ..."}}
                Return only JSON. No other commentary outside of the JSON.
                Generated queries should be line chart-friendly.
                Whatever column is selected as the x-axis should be a date or timestamp. Rename it as "time".
                Whatever column is selected as the y-axis should be a number - rename it as "total1".
                If there are multple series, the query should return them as total1, total2, total3, etc.
                """
                
        return prompt 
  
  
    def execute_function(self,socketio, session_id, convo_history, response_message, user_input, name, args):
 
        #print the function name and arguments
        print(f"Executing function '{name}' with arguments {args}")
        if name in self.function_mapping:
            func = self.function_mapping[name]
            data, metadata, commentary = func(socketio, session_id, convo_history, user_input, **args)
            return data, metadata, commentary
        else:
            raise ValueError(f"Function '{name}' not found.")
        
    def get_functions(self):
        return self.functions