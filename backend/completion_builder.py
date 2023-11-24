import json


bar_chart_advice = """
            Generated SQL queries should be bar chart-friendly. SQL generated should be SQLite compatible. 
            Whatever column is selected as the x-axis name as "X-Axis".
            Whatever column is selected as the y-axis should be a number - rename it as "Total". """

scatter_chart_advice = """ Generated SQL queries should be scatter chart-friendly. X and Y axis should be numbers. SQL generated should be SQLite compatible. 
            You can use "ORDER BY RANDOM() LIMIT 300" to sample the data randomly and keep the volume down for the front end.
            Whatever column is selected as the x-axis name as "X".
            Whatever column is seleted as the y-axis name as "Y".
            Whatever column is selected as the item we're plotting on X and Y should be named as Z.
            """

pie_chart_advice = """ Generated SQL queries should be pie chart-friendly. SQL generated should be SQLite compatible. 
            We're looking for two columns, one for the name, and one for the total. Make sure to rename them as "Name" and "Total".
            """

line_chart_advice = """ Generated SQL queries should be line chart-friendly. SQL generated should be SQLite compatible. 
            Whatever column is selected as the x-axis should be a date or timestamp. Rename it as "time".
            Whatever column is selected as the y-axis should be a number - rename it as "total1".
            If there are multple series, the query should return them as total1, total2, total3, etc."""

def build_basic_message_list(prompt):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    messages.append({"role": "system", "content": "You are helping the user explore data sets, and answer questions about them."}) 
    messages.append({"role": "user", "content": prompt})
    return messages

def build_message_list_for_sql_generation(prompt):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    messages.append({"role": "system", "content": "You are helping the user explore data sets and generate valid SQL queries."})
    messages.append({"role": "user", "content": prompt})
    return messages


def build_data_analysis_prompt(convo_history, user_input, data_str):
    return f"""
        Given the following data:
        {data_str}
        And the previous conversation history:
        {convo_history.messages}
        and the user's input:
        {user_input}
        Please very briefly comment on the data, given the context. Provide any analysis you think is relevant. Keep it to a couple hnundred words or less.
        When commenting on the data, stick to insights gleaned from the data, rather than the structure or schema of the data itself.
        """


def build_analysis_recommendation_prompt(convo_history, user_input, data_source_meta):
        prompt = f"""
                Given the following data source schema:
                {data_source_meta}
                please answer the following questions succinctly:
                {user_input}
                if needed, here's the most recent convo messages so far, if it helps to give context:
                {convo_history.messages}
                Recommend some interesting analysis that is possible using the data we have. Keep the descriptions short.
                The analysis should be possible using SQL, and particularly SQLite, but don't write the SQL. 
                Whatever analysis you suggest should be possible in a single SQlite compatible SQL query.
                Only suggest 2 or 3 ideas that are really high quality or will give insightful information. Keep it brief.
                Only suggest analysis based on the data we have in the meta data. Don't suggest analysis based on data we don't have.
                When suggsting visualisations, stick to basic visualisations like pie, bar, scatter, line. Don't suggest stacked bar charts, or other complex visualisations.
                The analysis should respect the following constraints for the different charts.
                {bar_chart_advice}
                {scatter_chart_advice}
                {pie_chart_advice}
                {line_chart_advice}

                """
                
        return prompt



def build_pipeline_prompt(convo_history, user_input, data_source_schemas, example_data_pipeline):
    
    current_data_pipeline = convo_history.get_current_data_pipeline()
    current_data_pipeline_str = ""
    if convo_history.get_current_data_pipeline() is not None:
        current_data_pipeline_str = current_data_pipeline

    prompt = f"""
    Given the following data source schemas:
    {data_source_schemas}

    and the previous conversation history:
    {convo_history.messages}

    Here is an example of a pipeline definition:
    {example_data_pipeline}

    Remember to replace the values in the example with the actual values you want to use, including the correct data source names.

    Here's some valid condition expressions. These will be executed by pandas query method, so they should be valid pandas query expressions.
    'age > 30',  # Rows where age is greater than 30
    'salary <= 50000',  # Rows where salary is less than or equal to 50,000
    'status == "Active"',  # Rows where status is 'Active'
    'department != "HR"',  # Rows where department is not 'HR'
    'age >= 25 and age <= 40',  # Rows where age is between 25 and 40 (inclusive)
    'salary > 20000 or age < 30',  # Rows where salary is more than 20,000 or age is less than 30
    'not (status == "Inactive")',  # Rows where status is not 'Inactive'
    'name.str.startswith("J")',  # Rows where name starts with 'J'
    'email.str.contains("@gmail.com")',  # Rows where email contains '@gmail.com'
    'date > "2023-01-01"',  # Rows where date is after January 1, 2023
    'index > 10',  # Rows where index is greater than 10
    'quantity <= 5 and product == "Widget"'  # Rows where quantity is less than or equal to 5 and product is 'Widget'
   
   
    please generate a valid pipeline JSON to help generate data, to the user's specification:
    {user_input}

    Consider iterating on the most recent pipeline generated.
    {current_data_pipeline_str}

    Make sure you respond with only the changes asked for by the user. Don't change anything else in the pipeline.

    Respond with only JSON pipeline. No other commentary outside of the JSON. Don't prefix the JSON object with "json" or any other text.
    Use the load_from_service method to load data rather than load.
    Give each step of the pipeline an id attribute, e.g. "id":"1" for the first step, "id":"2" for the second step, etc.
    """

    return prompt



def build_query_catalogue_prompt(convo_history, user_input, all_meta_data):
        prompt = f"""
                Given the following data source schemas:
                {all_meta_data}
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
                {{"data_source_names": ["datasource1"], "commentary": "Here's the data you're looking for."}}
                Return only JSON. No other commentary outside of the JSON. Don't prefix the JSON object with "json" or any other text.
                """
                
        return prompt

def table_sql_prompt(convo_history, user_input, data_source_meta):
        prompt = f"""
                Given the following data source schema:
                {data_source_meta}
                And the previous conversation history:
                {convo_history.messages}
                please generate JSON to help generate data, to the following questions succinctly:
                {user_input}
                if needed, here's the most recent SQL query generated, if it helps to give context:
                {convo_history.get_last_executed_query()}
                Return the answer in the following JSON format. Return only JSON. No other commentary outside of the JSON. Don't prefix the JSON object with "json" or any other text.
                E.g.
                {{"SQL": "select * from data_source_name where ..."}}
                SQL generated should be SQLite compatible. 
                Return only JSON. No other commentary outside of the JSON. Don't prefix the JSON object with "json" or any other text.
                """
                
        return prompt 

def build_data_source_inference_prompt(convo_history, user_input, all_meta_data):
        prompt = f"""
                Given the following data source schemas:
                {all_meta_data} 
                please determine the best single data source, to fetch data to answer the following questions succinctly:
                {user_input}
                Here's the conversation history so far, to help determine:
                {convo_history.messages}
                Return the answer in the following JSON format. Return only JSON. No other commentary outside of the JSON. Don't prefix the JSON object with "json" or any other text.
                {{"data_source": "data_source_name"}}
                """
                
        return prompt

def build_data_source_inference_prompt_for_multiple_data_sources(user_input, data_source_names):
        prompt = f"""
                Given the following data source schema names:
                {data_source_names} 
                please determine the best data sources, to fetch data to answer the following questions succinctly:
                {user_input}
                Return the answer in the following JSON format. Return only JSON. No other commentary outside of the JSON. Don't prefix the JSON object with "json" or any other text.
                {{"data_source_names": ["data_source_name1", "data_source_name2"]}}
                """
                
        return prompt

def add_custom_prompt_elements(prompt, data_source_name):
    finance_result_prompt_customisations = f"""
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
        prompt += finance_result_prompt_customisations
    

    if data_source_name == "restaurant_info":
        print("Restaurant info data source detected. Adding prompt additions.")
        prompt += """
        If the user asks about top restaurants, make sure to exclude restaurants with a rating of New.
        """

    return prompt



def bar_graph_sql_prompt(convo_history, user_input, data_source_meta):
    prompt = f"""
            Given the following data source schema:
            {data_source_meta}
            And the previous conversation history:
            {convo_history.messages}
            please generate JSON to help generate data, to the following questions succinctly:
            {user_input}
                if needed, here's the most recent SQL query generated, if it helps to give context:
            {convo_history.get_last_executed_query()}
            Return the answer in the following JSON format. Return only JSON. No other commentary outside of the JSON. Don't prefix the JSON object with "json" or any other text.
            E.g.
            {{"SQL": "select * from data_source_name where ..."}}
           {bar_chart_advice}
            """
            
    return prompt 

def scatter_graph_sql_prompt(convo_history, user_input, data_source_meta):
    prompt = f"""
            Given the following data source schema:
            {data_source_meta}
            And the previous conversation history:
            {convo_history.messages}
            please generate JSON to help generate data, to the following questions succinctly:
            {user_input}
                if needed, here's the most recent SQL query generated, if it helps to give context:
            {convo_history.get_last_executed_query()}
            Return the answer in the following JSON format. Return only JSON. No other commentary outside of the JSON. Don't prefix the JSON object with "json" or any other text.
            E.g.
            {{"SQL": "select * from data_source_name where ..."}}
            {scatter_chart_advice}
            """
            
    return prompt 

def pie_graph_sql_prompt(convo_history, user_input, data_source_meta):
    prompt = f"""
            Given the following data source schema:
            {data_source_meta}
            And the previous conversation history:
            {convo_history.messages}
            please generate JSON to help generate data, to the following questions succinctly:
            {user_input}
                if needed, here's the most recent SQL query generated, if it helps to give context:
            {convo_history.get_last_executed_query()}
            Return the answer in the following JSON format. Return only JSON. No other commentary outside of the JSON. Don't prefix the JSON object with "json" or any other text.
            E.g.
            {{"SQL": "select * from data_source_name where ..."}}
            {pie_chart_advice}
            """
            
    return prompt 
    
def line_graph_sql_prompt(convo_history, user_input, data_source_meta):
    prompt = f"""
            Given the following data source schema:
            {data_source_meta}
            And the previous conversation history:
            {convo_history.messages}
            please generate JSON to help generate data, to the following questions succinctly:
            {user_input}
            if needed, here's the most recent SQL query generated, if it helps to give context:
            {convo_history.get_last_executed_query()}
            Return the answer in the following JSON format. Return only JSON. No other commentary outside of the JSON. Don't prefix the JSON object with "json" or any other text.
            E.g.
            {{"SQL": "select * from data_source_name where ..."}}
            {line_chart_advice}
            """
            
    return prompt 