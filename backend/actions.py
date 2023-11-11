import json
from flask_socketio import SocketIO
import openai
from in_memory_db import InMemoryDB
from meta_data_service import MetaDataService
from typing import List, Dict, Any
import function_defs as function_defs
import completion_builder as completion_builder
from conversation_history import ConversationHistory

#constructor for a functions class
class ActionsManager:


    #constructor
    def __init__(self, current_model):
        self.current_model = current_model


        self.data_service = MetaDataService()

        self.functions = function_defs.get_open_ai_function_defs()

        self.function_mapping = {
            "query_data_catalogue": self.function_query_data_catalogue,
            "fetch_data": self.function_fetch_data,
            "fetch_meta_data": self.function_fetch_meta_data,
            "fetch_bar_chart_data": self.function_fetch_bar_chart_data,
            "fetch_line_chart_data": self.function_fetch_line_chart_data,
            "fetch_pie_chart_data": self.function_fetch_pie_chart_data,
            "fetch_scatter_chart_data": self.function_fetch_scatter_chart_data, 
            "comment_on_data": self.function_comment_on_data,
            "clear": self.function_clear,
            "recommend_analysis": self.function_recommend_analysis,  
            # Add more function mappings here...
        }


    def function_recommend_analysis(self, socketio, session_id, convo_history, user_input: str, data_source_name: str):
        
        data_source = self.data_service.get_data_source(data_source_name)
        if data_source is None:
            data_source_name, data_source = self.open_ai_infer_data_source(socketio, session_id, convo_history, user_input)

        #get the meta data for the data source
        data_source_meta = data_source["meta"]

        prompt = completion_builder.build_analysis_recommendation_prompt(convo_history, user_input, data_source_meta)
        messages = completion_builder.build_basic_message_list(prompt)
        response = openai.ChatCompletion.create(
            model=self.current_model,
            messages=messages
        )
        commentary = response['choices'][0]['message']['content']
        data = None
        metadata= None
        return data, metadata, commentary




           



   

    def function_comment_on_data(self, socketio, session_id, convo_history, user_input: str, data_source_name: str, query: str):

        #if we have both the data source name and the query, fetch the data
        if data_source_name is not None and query is not None:

            #add a limit to the query if it doesn't already have one. Stops wallet annihilation.
            if "LIMIT" not in query.upper():
                query += " LIMIT 100"

            #if it does have a limit, make sure the limit is 100 or less
            else:
                query = query.upper()
                limit_index = query.find("LIMIT")
                limit = int(query[limit_index + 5:])
                if limit > 100:
                    query = query[:limit_index + 5] + "100"
            

            data = self.data_service.query(query, data_source_name)
            metadata = None
            commentary = ""

            #emit that we're analysing the data
            progress_data = {'status': 'analysing_data', 'message': 'Analysing Data'}
            socketio.emit('progress', progress_data, room=session_id)

            #get the data set in a string format
            data_str = str(data)
            prompt = completion_builder.build_data_analysis_prompt(convo_history, user_input, data_str)
            messages = completion_builder.build_basic_message_list(prompt)
            response = openai.ChatCompletion.create(
                model=self.current_model,
                messages=messages
            )
            commentary = response['choices'][0]['message']['content']
            data = None
            metadata= None

            return data, metadata, commentary

   

    def function_clear(self, socketio, session_id, convo_history, user_input):
        convo_history = ConversationHistory()
        return None, None, "Conversation history cleared."


    #in a real system, this would be probably combine some embeddings search with a metadata service. 
    #we'll fake it for now. 
    def function_query_data_catalogue(self, socketio, session_id, convo_history, user_input : str):

        all_meta_data = self.data_service.get_all_meta_data()

        prompt = completion_builder.build_query_catalogue_prompt(convo_history, user_input, all_meta_data)

        #print the user input we're using to generate a response
        print(f"User input: {user_input}")
        messages = completion_builder.build_basic_message_list(prompt)
        response = openai.ChatCompletion.create(
            model=self.current_model,
            messages=messages
        )
        commentary = response['choices'][0]['message']['content']
        commentary = self.check_for_json_tag(commentary)
        data = None
        metadata= None
        return data, metadata, commentary

   

    #fetch actual data. fires off an open ai call to infer data source if we didn't infer in the function call
    def function_fetch_data(self, socketio, session_id, convo_history: ConversationHistory, user_input, data_source_name):
        #if data source is not none
        commentary = ""
        data_source = self.data_service.get_data_source(data_source_name)
        if data_source is None:
            data_source_name, data_source = self.open_ai_infer_data_source(socketio, session_id, convo_history, user_input)
           
           
        response = self.open_ai_generate_sql(socketio, session_id, convo_history, user_input,data_source["meta"], completion_builder.table_sql_prompt(convo_history, user_input, data_source["meta"]))

        print(response)
        data = self.data_service.query(response["SQL"], data_source_name)
        convo_history.set_last_executed_query(response["SQL"])
        metadata = None
        commentary = f"DataQuery: Data source name: {data_source_name}, Query: {response['SQL']}"
        return data, metadata, commentary
    
    def function_fetch_scatter_chart_data(self, socketio, session_id, convo_history, user_input, data_source_name, x_axis_title,y_axis_title,chart_title):
        #if data source is not none
        commentary = ""
        data_source = self.data_service.get_data_source(data_source_name)
        if data_source is None:
            data_source_name, data_source = self.open_ai_infer_data_source(socketio, session_id, convo_history, user_input)
           
           
        response = self.open_ai_generate_sql(socketio, session_id, convo_history, user_input,data_source["meta"], completion_builder.scatter_graph_sql_prompt(convo_history, user_input, data_source["meta"]))
        convo_history.set_last_executed_query(response["SQL"])
        print(response)
        data = self.data_service.query(response["SQL"], data_source_name)
 

        #let's put the chart axis and title in a JSON object in metadata
        metadata = {"x_axis_title": x_axis_title, "y_axis_title": y_axis_title, "chart_title": chart_title}
       
        commentary = f"DataQuery: Data source name: {data_source_name}, Query: {response['SQL']}"
        return data, metadata, commentary
    
    def function_fetch_pie_chart_data(self, socketio, session_id, convo_history, user_input, data_source_name,chart_title):
        #if data source is not none
        commentary = ""
        data_source = self.data_service.get_data_source(data_source_name)
        if data_source is None:
            data_source_name, data_source = self.open_ai_infer_data_source(socketio, session_id, convo_history, user_input)
           
           
        response = self.open_ai_generate_sql(socketio, session_id, convo_history, user_input,data_source["meta"], completion_builder.pie_graph_sql_prompt(convo_history, user_input, data_source["meta"]))
        convo_history.set_last_executed_query(response["SQL"])
        print(response)
        data = self.data_service.query(response["SQL"], data_source_name)

        #let's put the chart axis and title in a JSON object in metadata
        metadata = {"chart_title": chart_title}
       
        commentary = f"DataQuery: Data source name: {data_source_name}, Query: {response['SQL']}"
        return data, metadata, commentary
    
    def function_fetch_bar_chart_data(self, socketio, session_id, convo_history, user_input, data_source_name, x_axis_title,y_axis_title,chart_title):
        #if data source is not none
        commentary = ""
        data_source = self.data_service.get_data_source(data_source_name)
        if data_source is None:
            data_source_name, data_source = self.open_ai_infer_data_source(socketio, session_id, convo_history, user_input)
           
           
        response = self.open_ai_generate_sql(socketio, session_id, convo_history, user_input,data_source["meta"], completion_builder.bar_graph_sql_prompt(convo_history, user_input, data_source["meta"]))
        convo_history.set_last_executed_query(response["SQL"])
        print(response)
        data = self.data_service.query(response["SQL"], data_source_name)

        #let's put the chart axis and title in a JSON object in metadata
        metadata = {"x_axis_title": x_axis_title, "y_axis_title": y_axis_title, "chart_title": chart_title}
       
        commentary = f"DataQuery: Data source name: {data_source_name}, Query: {response['SQL']}"
        return data, metadata, commentary
    
    def function_fetch_line_chart_data(self, socketio, session_id, convo_history: ConversationHistory, user_input, data_source_name,x_axis_title,y_axis_title,chart_title):
        #if data source is not none
        commentary = ""
        data_source = self.data_service.get_data_source(data_source_name)
        if data_source is None:
            data_source_name, data_source = self.open_ai_infer_data_source(socketio, session_id, convo_history, user_input)
           
           
        response = self.open_ai_generate_sql(socketio, session_id, convo_history, user_input,data_source["meta"], completion_builder.line_graph_sql_prompt(convo_history, user_input, data_source["meta"]))
        convo_history.set_last_executed_query(response["SQL"])
        print(response)
        data = self.data_service.query(response["SQL"], data_source_name)
         #let's put the chart axis and title in a JSON object in metadata
        metadata = {"x_axis_title": x_axis_title, "y_axis_title": y_axis_title, "chart_title": chart_title}
       
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

        all_meta_data = self.data_service.get_all_meta_data()
        prompt = completion_builder.build_data_source_inference_prompt(convo_history, user_input, all_meta_data)

        #print the user input we're using to generate a response
        print(f"User input: {user_input}")
        messages = completion_builder.build_basic_message_list(prompt)
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

        prompt = completion_builder.add_custom_prompt_elements(prompt, data_source_name)

        #print the user input we're using to generate a response
        print(f"User input: {user_input}")

        messages = completion_builder.build_message_list_for_sql_generation(prompt)

        response = openai.ChatCompletion.create(
            model=self.current_model,
            messages=messages
        )
        output = response['choices'][0]['message']['content']

        #GPT-4-Turbo generally tags JSON output with "json" at the start of the string.
        #Remove the json tagging if it exists.
        output = self.check_for_json_tag(output)

        return json.loads(output) 
    

    def check_for_json_tag(self, output):
        if output.startswith("```json"):
            output = output.replace("```json", "")
            output = output.replace("```", "")
        return output

  
    def execute_function(self,socket_io: SocketIO, session_id: str,conversation_history: ConversationHistory, response_message: Dict[str,Any], user_input: str, name: str, args) -> tuple[List[Dict[str, Any]], Dict[str, Any], str ]:
 
        #print the function name and arguments
        print(f"Executing function '{name}' with arguments {args}")
        if name in self.function_mapping:
            func = self.function_mapping[name]
            data, metadata, commentary = func(socket_io, session_id, conversation_history, user_input, **args)
            return data, metadata, commentary
        else:
            raise ValueError(f"Function '{name}' not found.")
        
    def get_functions(self):
        return self.functions