import json
from in_memory_db import InMemoryDB
from typing import List, Dict, Any

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




    def add_data_source(self, data_source_json_path, datasource_csv_path):

        # Load the metadata from JSON files
        data_source_meta = self.load_json(data_source_json_path)
        
        # Create in-memory databases
        data_source_db = InMemoryDB()
        data_source_db.load_csv_to_db(datasource_csv_path, data_source_meta['name'])

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
    
    #get all meta data concatenated together in a single string
    def get_all_meta_data(self):
        meta_data = ""
        for data_source in self.data_sources:
            meta_data += str(self.data_sources[data_source]['meta'])
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
    
    # Example usage
#repository = DataRepository()
#restaurant_info = repository.get_data_source('restaurant_info')
#if restaurant_info:
#    meta = restaurant_info['meta']
#    db = restaurant_info['db']

