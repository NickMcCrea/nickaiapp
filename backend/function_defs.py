def get_open_ai_function_defs():
        return [      
        {
         "name": "query_data_catalogue",
            "description": f"""Use this function to answer user questions about what data sources we have available.
                            For example, the user may ask about data sources, or ask about a specific data source, or attribute. 
                            Or they may ask about the data catalogue. 
                            """,
          "parameters": {
                "type": "object",
                "properties": {}
            }
        },
        {
         "name": "recommend_analysis",
            "description": f"""Use this when the user asks for a recommendation for analysis to do on the dataset.
                            """,
          "parameters": {
                "type": "object",
                "properties": 
                {
                    "data_source_name": {
                        "type": "string",
                        "description": "The name of the data source to analyse."
                    }
                }
            }
        },
        {
         "name": "comment_on_data",
            "description": f"""Use this function to comment on specific data.
                            For example, the user may ask for analysis or commentary on a data set that's just been returned.
                            """,
          "parameters": {
                "type": "object",
                "properties": 
                {
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
        },
        {
         "name": "clear",
            "description": f"""Use this function to clear the conversation history, and start a new conversation.
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
         },
         {
         "name": "fetch_scatter_chart_data",
            "description": f"""Use this function when a user asks for a question that requires a scatter chart or scatter plot.
                            Users may ask to see the relationship between two values, e.g. "Can you show me the relationship between delivery times and customer ratings?"
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
         },
         {
         "name": "fetch_pie_chart_data",
            "description": f"""Use this function when a user asks for a question that requires a pie chart or pie graph.
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
                    },
                     "chart_title": {
                        "type": "string",
                        "description": "Suggested title for the chart. Keep it short and sweet."
                    }
                }
            }
         }, 
        ]