
def generate_datasources_function(data_sources_string):
    
    return {
         "name": "get_data_sources",
            "description": "Use this function to answer user questions about what data sources we have available.",
            "parameters": {
                "type": "object",
                "properties": {
                    "datasourcelist": {
                        "type": "string",
                        "description": f"""
                                A list of data sources we have available, in a JSON format. 
                                {data_sources_string}
                                Ignore the connection info and the type of data source (e.g. SQlite, CSV, etc.) Concentrate on the name and description, and the tables and columns available.
                                """,
                    }
                },
                "required": ["datasourcelist"],
            },
    }