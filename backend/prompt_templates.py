
def generate_datasources_prompt(data_sources_string, query):
    
    prompt = f"""Answer the user's question about data sources. 
    The user asked: "{query}". 
    Ignore the connectivity details or the type of underlying data source (e.g. sqlite or csv).
    Answer succinctly and in plain English.
    Don't reference the underlying JSON file, only the data sources themselves.
    The data sources we have available are: {data_sources_string}"""
    return prompt
    