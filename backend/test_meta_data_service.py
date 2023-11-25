import unittest
from unittest.mock import patch, mock_open, MagicMock
import pandas as pd
from io import StringIO
from in_memory_db import InMemoryDB
from meta_data_service import MetaDataService

class TestMetaDataService(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='{"name": "test_data_source", "fields": []}')
    def test_load_json(self, mock_file):
        service = MetaDataService()
        result = service.load_json('fake_path.json')
        self.assertEqual(result, {"name": "test_data_source", "fields": []})
        mock_file.assert_called_with('fake_path.json', 'r')

    @patch('builtins.open', new_callable=mock_open, read_data='{"name": "test_data_source", "fields": []}')
    @patch('in_memory_db.InMemoryDB.load_csv_to_db')
    @patch('meta_data_service.MetaDataService.load_json')
    def test_add_data_source(self, mock_load_json, mock_load_csv_to_db, mock_file):
        mock_load_json.return_value = {"name": "test_data_source", "fields": []}
        service = MetaDataService()
        service.add_data_source('datasources/test.json', 'datasources/test.csv')
        self.assertIn('test_data_source', service.data_sources)
        mock_load_csv_to_db.assert_called_once()

    def test_get_data_source(self):
        service = MetaDataService()
        service.data_sources = {'test': 'dummy_data'}
        result = service.get_data_source('test')
        self.assertEqual(result, 'dummy_data')

    def test_get_all_data_source_names(self):
        service = MetaDataService()
        service.data_sources = {'test1': {}, 'test2': {}}
        result = service.get_all_data_source_names()
        self.assertListEqual(result, ['test1', 'test2'])

    def test_get_all_meta_data(self):
        service = MetaDataService()
        service.data_sources = {'test1': {'meta': 'meta1'}, 'test2': {'meta': 'meta2'}}
        result = service.get_all_meta_data()
        self.assertListEqual(result, ['meta1', 'meta2'])

    def test_get_meta_data_for_multiple_data_sources(self):
        service = MetaDataService()
        service.data_sources = {'test1': {'meta': 'meta1'}, 'test2': {'meta': 'meta2'}}
        result = service.get_meta_data_for_multiple_data_sources(['test1', 'test2'])
        self.assertListEqual(result, ['meta1', 'meta2'])

    @patch('in_memory_db.InMemoryDB.query')
    def test_query(self, mock_query):
        mock_db = MagicMock()
        mock_query.return_value = []  # Assuming query returns an empty list for simplicity

        service = MetaDataService()
        service.data_sources = {'test': {'db': mock_db}}
        
        service.query('SELECT * FROM test', 'test')
        
        mock_db.query.assert_called_once_with('SELECT * FROM test')


    @patch('pandas.api.types.is_string_dtype', return_value=True)
    @patch('pandas.api.types.is_integer_dtype', return_value=False)
    @patch('pandas.api.types.is_float_dtype', return_value=False)
    @patch('pandas.api.types.is_bool_dtype', return_value=False)
    @patch('pandas.api.types.is_datetime64_any_dtype', return_value=False)
    def test_infer_field_type_string(self, mock_date, mock_bool, mock_float, mock_int, mock_str):
        dtype = pd.Series(['a', 'b', 'c']).dtype
        result = MetaDataService._infer_field_type(dtype)
        self.assertEqual(result, 'STRING')

    @patch('pandas.api.types.is_string_dtype', return_value=False)
    @patch('pandas.api.types.is_integer_dtype', return_value=True)
    @patch('pandas.api.types.is_float_dtype', return_value=False)
    @patch('pandas.api.types.is_bool_dtype', return_value=False)
    @patch('pandas.api.types.is_datetime64_any_dtype', return_value=False)
    def test_infer_field_type_integer(self, mock_date, mock_bool, mock_float, mock_int, mock_str):
        dtype = pd.Series([1, 2, 3]).dtype
        result = MetaDataService._infer_field_type(dtype)
        self.assertEqual(result, 'INTEGER')

    @patch('in_memory_db.InMemoryDB.load_df_to_db')
    def test_persist_data_source(self, mock_load_df_to_db):
        service = MetaDataService()
        df = pd.DataFrame({'a': [1, 2, 3], 'b': ['x', 'y', 'z']})
        service.persist_data_source('test_data', df)
        self.assertIn('test_data', service.data_sources)
        mock_load_df_to_db.assert_called_once()


    

    

    



if __name__ == '__main__':
    unittest.main()
