# Define each function as a separate dictionary

query_data_catalogue = {
    "name": "query_data_catalogue",
    "description": "Use this function to answer user questions about what data sources we have available.",
    "parameters": {
        "type": "object",
        "properties": {}
    }
}

recommend_analysis = {
    "name": "recommend_analysis",
    "description": "Use this when the user asks for a recommendation for analysis to do on the dataset.",
    "parameters": {
        "type": "object",
        "properties": {
            "data_source_name": {
                "type": "string",
                "description": "The name of the data source to analyse."
            }
        }
    }
}

comment_on_data = {
    "name": "comment_on_data",
    "description": "Use this function to comment on specific data.",
    "parameters": {
        "type": "object",
        "properties": {
            "data_source_name": {
                "type": "string",
                "description": "The name of the data source to fetch from"
            },
            "query": {
                "type": "string",
                "description": "The query that was used to fetch the data"
            }
        }
    }
}

clear = {
    "name": "clear",
    "description": "Use this function to clear the conversation history, and start a new conversation.",
    "parameters": {
        "type": "object",
        "properties": {}
    }
}

fetch_meta_data = {
    "name": "fetch_meta_data",
    "description": "Use this function to retrieve meta data about a data source.",
    "parameters": {
        "type": "object",
        "properties": {
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
}

fetch_data = {
    "name": "fetch_data",
    "description": "Use this function when a user asks for a question that requires a data query.",
    "parameters": {
        "type": "object",
        "properties": {
            "data_source_name": {
                "type": "string",
                "description": "The name of the data source to fetch data from."
            }
        }
    }
}

ask_panel_fetch_data = {
    "name": "ask_panel_fetch_data",
    "description": "Use this function when a user asks for a question that requires a data query.",
    "parameters": {
        "type": "object",
        "properties": {
            "data_source_name": {
                "type": "string",
                "description": "The name of the data source to fetch data from."
            }
        }
    }
}

fetch_bar_chart_data = {
    "name": "fetch_bar_chart_data",
    "description": "Use this function when a user asks for a question that requires a bar chart or bar graph.",
    "parameters": {
        "type": "object",
        "properties": {
            "data_source_name": {
                "type": "string",
                "description": "The name of the data source to fetch data from."
            },
            "x_axis_title": {
                "type": "string",
                "description": "Suggested name for the x-axis"
            },
            "y_axis_title": {
                "type": "string",
                "description": "Suggested name for the y-axis"
            },
            "chart_title": {
                "type": "string",
                "description": "Suggested title for the chart. Keep it short and sweet."
            }
        }
    }
}

fetch_line_chart_data = {
    "name": "fetch_line_chart_data",
    "description": "Use this function when a user asks for a question that requires a line chart or time series.",
    "parameters": {
        "type": "object",
        "properties": {
            "data_source_name": {
                "type": "string",
                "description": "The name of the data source to fetch data from."
            },
            "x_axis_title": {
                "type": "string",
                "description": "Suggested name for the x-axis"
            },
            "y_axis_title": {
                "type": "string",
                "description": "Suggested name for the y-axis"
            },
            "chart_title": {
                "type": "string",
                "description": "Suggested title for the chart. Keep it short and sweet."
            }
        }
    }
}

fetch_scatter_chart_data = {
    "name": "fetch_scatter_chart_data",
    "description": "Use this function when a user asks for a question that requires a scatter chart or scatter plot.",
    "parameters": {
        "type": "object",
        "properties": {
            "data_source_name": {
                "type": "string",
                "description": "The name of the data source to fetch data from."
            },
            "x_axis_title": {
                "type": "string",
                "description": "Suggested name for the x-axis"
            },
            "y_axis_title": {
                "type": "string",
                "description": "Suggested name for the y-axis"
            },
            "chart_title": {
                "type": "string",
                "description": "Suggested title for the chart. Keep it short and sweet."
            }
        }
    }
}

fetch_pie_chart_data = {
    "name": "fetch_pie_chart_data",
    "description": "Use this function when a user asks for a question that requires a pie chart or pie graph.",
    "parameters": {
        "type": "object",
        "properties": {
            "data_source_name": {
                "type": "string",
                "description": "The name of the data source to fetch data from."
            },
            "chart_title": {
                "type": "string",
                "description": "Suggested title for the chart. Keep it short and sweet."
            }
        }
    }
}

create_workspace = {
    "name": "create_workspace",
    "description": "Use this function when a user asks to create a workspace, or make a new data set.",
    "parameters": {
        "type": "object",
        "properties": {
            "prompt_user_for_data": {
                "type": "string",
                "description": "Very briefly prompt the user to start defining the data set - e.g. 'What data set would you like to create?'"
            }
        }
    }
}




define_new_data_set = {

    "name": "define_new_data_set",
    "description": """Use this function to generate or edit a pipeline definition, when the user wants to define a new data set. 
                    Use this when the user specifies a step in the pipeline, e.g load, sort, filter, join, persist etc.
                    Don't go beyond what the user has specified - let the user define the pipeline definition incrementally.
                    Use this when the user is incrementally altering a pipeline also - regenerate it.
                    """,
     "parameters": {
        "type": "object",
        "properties": {}
    }

}

create_new_data_set = {
    "name": "create_new_data_set",
    "description": "Use this function to execute a pipeline definition, and actually create and persist a new data set for real. Use this when the user finalizes the pipeline definition, and wants to create a new data set.",
    "parameters": {
        "type": "object",
        "properties": {
            "data_source_name": {
                "type": "string",
                "description": "New name for the data source. Don't use the same name as an existing data source."
            },
             "data_source_description": {
                "type": "string",
                "description": "Description of the new data source."
            }
        }
    }


    
}


#functions for the "Ask" panel in the UI
def data_set_lock_functions():
    return [
        ask_panel_fetch_data,
    ]


#standard functions
def default_functions():
    return [
        query_data_catalogue, 
        recommend_analysis, 
        comment_on_data, 
        clear, 
        fetch_meta_data, 
        fetch_data, 
        fetch_bar_chart_data, 
        fetch_line_chart_data, 
        fetch_scatter_chart_data, 
        fetch_pie_chart_data, 
        create_workspace
    ]

#Functions for the workspace functionality
def workspace_functions():
    return [
        define_new_data_set,
        create_new_data_set
    ]



# Now, you can call get_open_ai_function_defs() to get all the functions except 'exit_workspace'
