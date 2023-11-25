import unittest
from unittest.mock import patch
import pandas as pd
from data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):

    def setUp(self):
        # Common setup for all tests, if needed
        pass

    def test_load_from_data(self):
        # Test the load_from_data method
        meta_data = {'fields': [{'fieldName': 'date', 'fieldType': 'DATE'}, {'fieldName': 'value', 'fieldType': 'INTEGER'}]}
        data = [{'date': '2021-01-01', 'value': 10}, {'date': '2021-01-02', 'value': 20}]
        expected_df = pd.DataFrame({'date': pd.to_datetime(['2021-01-01', '2021-01-02']), 'value': pd.Series([10, 20], dtype='Int64')})
        result_df = DataProcessor.load_from_data(meta_data, data)
        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_filter(self):
        # Test the filter method
        df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        conditions = {'a': {'equals': 2}}
        expected_df = pd.DataFrame({'a': [2], 'b': [5]}, index=[1])
        result_df = DataProcessor.filter(df, conditions)
        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_join(self):
        # Test the join method
        df1 = pd.DataFrame({'key': [1, 2], 'value1': [10, 20]})
        df2 = pd.DataFrame({'key': [1, 2], 'value2': [30, 40]})
        expected_df = pd.DataFrame({'key': [1, 2], 'value1': [10, 20], 'value2': [30, 40]})
        result_df = DataProcessor.join(df1, df2, on='key')
        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_aggregate(self):
        # Test the aggregate method
        df = pd.DataFrame({'group': ['A', 'A', 'B'], 'value': [10, 20, 30]})
        group_by = ['group']
        aggregations = [{'column': 'value', 'aggregation': 'sum'}]
        expected_df = pd.DataFrame({'group': ['A', 'B'], 'value': [30, 30]})
        result_df = DataProcessor.aggregate(df, group_by, aggregations)
        pd.testing.assert_frame_equal(result_df, expected_df)

    
    def test_select_columns(self):
        # Test the select_columns method
        df = pd.DataFrame({'a': [1, 2], 'b': [3, 4], 'c': [5, 6]})
        columns = ['a', 'c']
        expected_df = pd.DataFrame({'a': [1, 2], 'c': [5, 6]})
        result_df = DataProcessor.select_columns(df, columns)
        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_rename_columns(self):
        # Test the rename_columns method
        df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        rename_map = {'a': 'x', 'b': 'y'}
        expected_df = pd.DataFrame({'x': [1, 2], 'y': [3, 4]})
        result_df = DataProcessor.rename_columns(df, rename_map)
        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_sort_data(self):
    # Test the sort_data method
        df = pd.DataFrame({'a': [2, 1, 3]}, index=[1, 0, 2])
        by = ['a']
        expected_df = pd.DataFrame({'a': [1, 2, 3]}, index=[0, 1, 2])
        result_df = DataProcessor.sort_data(df, by)
        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_add_columns(self):
        # Test the add_columns method
        df = pd.DataFrame({'a': [1, 2]})
        new_columns = {'b': lambda df: df['a'] * 2, 'c': 3}
        expected_df = pd.DataFrame({'a': [1, 2], 'b': [2, 4], 'c': [3, 3]})
        result_df = DataProcessor.add_columns(df, new_columns)
        pd.testing.assert_frame_equal(result_df, expected_df)

    
    def test_apply_conditional_logic_basic(self):
        # Basic condition test
        df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        condition_str = 'a > 1'
        update_values = {'b': 5}
        expected_df = pd.DataFrame({'a': [1, 2], 'b': [3, 5]})
        result_df = DataProcessor.apply_conditional_logic(df, condition_str, update_values)
        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_apply_conditional_logic_multiple_conditions(self):
        # Multiple conditions test
        df = pd.DataFrame({'a': [1, 2], 'b': [3, 4], 'c': [5, 6]})
        condition_str = 'a > 1 and b < 5'
        update_values = {'c': 10}
        expected_df = pd.DataFrame({'a': [1, 2], 'b': [3, 4], 'c': [5, 10]})
        result_df = DataProcessor.apply_conditional_logic(df, condition_str, update_values)
        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_apply_conditional_logic_no_match(self):
        # Testing no match
        df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        condition_str = 'a > 2'
        update_values = {'b': 5}
        expected_df = df.copy()
        result_df = DataProcessor.apply_conditional_logic(df, condition_str, update_values)
        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_apply_conditional_logic_all_match(self):
        # Testing all match
        df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        condition_str = 'a > 0'
        update_values = {'b': 5}
        expected_df = pd.DataFrame({'a': [1, 2], 'b': [5, 5]})
        result_df = DataProcessor.apply_conditional_logic(df, condition_str, update_values)
        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_apply_conditional_logic_multiple_updates(self):
        # Testing multiple updates
        df = pd.DataFrame({'a': [1, 2], 'b': [3, 4], 'c': [5, 6]})
        condition_str = 'a > 1'
        update_values = {'b': 7, 'c': 8}
        expected_df = pd.DataFrame({'a': [1, 2], 'b': [3, 7], 'c': [5, 8]})
        result_df = DataProcessor.apply_conditional_logic(df, condition_str, update_values)
        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_apply_conditional_logic_edge_case(self):
        # Testing edge case: empty DataFrame
        df = pd.DataFrame(columns=['a', 'b'])
        condition_str = 'a > 1'
        update_values = {'b': 5}
        expected_df = df.copy()
        result_df = DataProcessor.apply_conditional_logic(df, condition_str, update_values)
        pd.testing.assert_frame_equal(result_df, expected_df)
 
    def tearDown(self):
        # Tear down (cleanup) actions if required
        pass

if __name__ == '__main__':
    unittest.main()
