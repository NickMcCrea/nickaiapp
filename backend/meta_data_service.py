import json
from in_memory_db import InMemoryDB
from typing import List, Dict, Any
import pandas as pd

class MetaDataService:
    def __init__(self):
        self.data_sources = {}
        self.initialize_data_sources()

    def initialize_data_sources(self):
        # Load the metadata from JSON files
        self.add_data_source('datasources/restaurants.json', 'datasources/restaurants.csv')
        self.add_data_source('datasources/counterparties.json', 'datasources/counterparties.csv')
        self.add_data_source('datasources/products.json', 'datasources/products.csv')
        self.add_data_source('datasources/nicktrialbalance.json', 'datasources/nicktrialbalance.csv')
        self.add_data_source('datasources/top_songs.json', 'datasources/top_songs.csv')
        self.add_data_source('datasources/financialresults.json', 'datasources/financialresults.csv')
        self.add_data_source('datasources/nba_stats.json', 'datasources/nba_stats.csv')
        self.add_data_source('datasources/netflix.json', 'datasources/netflix.csv')
        self.add_data_source('datasources/football.json', 'datasources/football.csv')
        self.add_data_source('datasources/fifa.json', 'datasources/fifa.csv')
        #self.add_data_source('datasources/glbal.json', 'datasources/glbal.csv')
     


    def add_data_source(self, data_source_json_path, datasource_csv_path):

        # Load the metadata from JSON files
        data_source_meta = self.load_json(data_source_json_path)
        
        # Create in-memory databases
        data_source_db = InMemoryDB()
        data_source_db.load_csv_to_db(datasource_csv_path, data_source_meta)

        # Add the metadata and databases to the data_sources dictionary
        self.data_sources[data_source_meta['name']] = {
            'meta': data_source_meta,
            'db': data_source_db,
        }

    def load_json(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
        

    def get_data_source(self, name):
        return self.data_sources.get(name, None)
    
    #get all meta data in a list
    def get_all_meta_data(self):
        meta_data = []
        for data_source in self.data_sources:
            meta_data.append(self.data_sources[data_source]['meta'])
        return meta_data
       

    #we should return a list of JSON metadata objects
    def get_all_meta_data_as_json(self):
        meta_data = []
        for data_source in self.data_sources:
            meta_data.append(self.data_sources[data_source]['meta'])
        return meta_data
        
    def get_meta_data_for_multiple_data_sources(self, data_source_names):
        meta_data = []
        for data_source_name in data_source_names:
            meta_data.append(self.data_sources[data_source_name]['meta'])
        return meta_data

    def query(self, sql_query: str, data_source_name: str) -> List[Dict[str, Any]]:
        # Retrieve the data source by name
        data_source = self.get_data_source(data_source_name)
        
        # If the data source exists, execute the query
        if data_source:
            db = data_source['db']
            return db.query(sql_query)
        else:
            raise ValueError(f"Data source '{data_source_name}' not found.")
        

    def persist_data_source(self, name, df: pd.DataFrame, description="", category="Miscellaneous"):
        """
        Persist a DataFrame as a new data source in the MetaDataService.

        :param name: Name of the new data source.
        :param df: DataFrame to be persisted.
        :param description: Description of the new data source.
        :param category: Category of the new data source.
        """
        # Generate metadata based on DataFrame's columns
        fields = []
        for column in df.columns:
            field_type = self._infer_field_type(df[column].dtype)
            fields.append({
                "fieldName": column,
                "fieldDescription": "",  # Leaving individual field descriptions blank for now
                "fieldType": field_type
            })

        meta_data = {
            "name": name,
            "description": description,
            "category": category,
            "fields": fields
        }

        # Create an in-memory database and load the DataFrame
        data_source_db = InMemoryDB()
        data_source_db.load_df_to_db(df, meta_data)

        # Add the metadata and database to the data sources dictionary
        self.data_sources[name] = {
            'meta': meta_data,
            'db': data_source_db,
        }

    @staticmethod
    def _infer_field_type(dtype):
        """
        Infer the field type from pandas dtype.

        :param dtype: Pandas data type of a DataFrame column.
        :return: String representing the field type.
        """
        if pd.api.types.is_string_dtype(dtype):
            return 'STRING'
        elif pd.api.types.is_integer_dtype(dtype):
            return 'INTEGER'
        elif pd.api.types.is_float_dtype(dtype):
            return 'FLOAT'
        elif pd.api.types.is_bool_dtype(dtype):
            return 'BOOLEAN'
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            return 'DATE'
        else:
            return 'STRING'  # Default to STRING for unsupported types
    
    # Example usage
#repository = DataRepository()
#restaurant_info = repository.get_data_source('restaurant_info')
#if restaurant_info:
#    meta = restaurant_info['meta']
#    db = restaurant_info['db']

