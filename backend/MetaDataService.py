import json
from in_memory_db import InMemoryDB

class MetaDataService:
    def __init__(self):
        self.data_sources = {}
        self.initialize_data_sources()

    def initialize_data_sources(self):
        # Load the metadata from JSON files
        top_songs_meta = self.load_json("datasources/top_songs.json")
        restaurants_meta = self.load_json("datasources/restaurants.json")
        trial_balance_meta = self.load_json("datasources/nicktrialbalance.json")
        counterparties_meta = self.load_json("datasources/counterparties.json")
        products_meta = self.load_json("datasources/products.json")
        
        # Create in-memory databases
        top_song_data_db = InMemoryDB()
        top_song_data_db.load_csv_to_db('datasources/top_songs.csv', 'spotify_track_data')

        restaurants_data_db = InMemoryDB()
        restaurants_data_db.load_csv_to_db('datasources/restaurants.csv', 'restaurant_info')

        trial_balance_data_db = InMemoryDB()
        trial_balance_data_db.load_csv_to_db('datasources/nicktrialbalance.csv', 'trial_balance_data')

        counterparties_data_db = InMemoryDB()
        counterparties_data_db.load_csv_to_db('datasources/counterparties.csv', 'counterparty_data')

        products_data_db = InMemoryDB()
        products_data_db.load_csv_to_db('datasources/products.csv', 'product_data')

        # Add the metadata and databases to the data_sources dictionary
        self.data_sources[top_songs_meta['name']] = {
            'meta': top_songs_meta,
            'db': top_song_data_db,
        }

        self.data_sources[restaurants_meta['name']] = {
            'meta': restaurants_meta,
            'db': restaurants_data_db
        }

        self.data_sources[trial_balance_meta['name']] = {
            'meta': trial_balance_meta,
            'db': trial_balance_data_db
        }

        self.data_sources[counterparties_meta['name']] = {
            'meta': counterparties_meta,
            'db': counterparties_data_db
        }

        self.data_sources[products_meta['name']] = {
            'meta': products_meta,
            'db': products_data_db
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
    
    def query(self, sql_query, data_source_name):
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

