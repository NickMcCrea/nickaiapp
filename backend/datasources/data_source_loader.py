import json
from typing import Dict, Any
from .data_source import DataSource

class DataSourceLoader:
    def __init__(self):
        self.data_sources = {}  # To store DataSource objects in memory

    def load_from_file(self, file_path: str):
        """
        Load data source from a JSON file and store it in memory.
        """
        with open(file_path, 'r') as f:
            data_source_dict = json.load(f)
            name = data_source_dict.get('name')
            if name:
                # Create a DataSource object
                data_source_obj = DataSource(
                    name=data_source_dict.get('name'),
                    description=data_source_dict.get('description'),
                    type=data_source_dict.get('type'),
                    connectionInfo=data_source_dict.get('connectionInfo'),
                    tables=data_source_dict.get('tables')
                )
                # Store the DataSource object
                self.data_sources[name] = data_source_obj
            else:
                raise ValueError(f"Data source in {file_path} does not contain a 'name' field.")

    def get_data_source(self, name: str) -> Any:
        """
        Retrieve a data source object by its name.
        """
        return self.data_sources.get(name, None)
    
    #get_data_source_string, a method which returns all the data sources details as a single string
    def get_data_source_string(self) -> str:
       
        data_source_string = ""
        for data_source_name, data_source_obj in self.data_sources.items():
           data_source_string += f"Data source details: {data_source_obj}\n"
        return data_source_string

