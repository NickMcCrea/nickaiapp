import unittest
from unittest.mock import Mock, patch
from data_processor import DataProcessor
from meta_data_service import MetaDataService
from data_pipeline_executor import DataPipelineExecutor
import pandas as pd

class TestDataPipelineExecutor(unittest.TestCase):

    
    def setUp(self):
        self.mock_processor = Mock(spec=DataProcessor)
        self.mock_meta_data_service = Mock(spec=MetaDataService)
        self.executor = DataPipelineExecutor(self.mock_processor, self.mock_meta_data_service)

    def test_load_from_service(self):
        # Setup
        test_data = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        self.mock_meta_data_service.get_data_source.return_value = {
            'meta': {'fields': [{'fieldName': 'col1', 'fieldType': 'INTEGER'}]},
            'db': Mock(query=Mock(return_value=test_data))
        }
        # Here's the change: specify the return value for load_from_data
        self.mock_processor.load_from_data.return_value = test_data

        # Execute
        pipeline_def = [{'action': 'load_from_service', 'params': {'name': 'source1', 'output_name': 'df_initial'}}]
        result = self.executor.run(pipeline_def)

        # Assert
        self.mock_processor.load_from_data.assert_called_once()
        self.assertIn('df_initial', result)
        self.assertEqual(result['df_initial'].shape, test_data.shape)

    def test_filter(self):
        # Setup
        initial_data = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        filtered_data = initial_data[initial_data['a'] > 1]
        self.mock_processor.filter.return_value = filtered_data

        # Define a pipeline with load_from_service followed by filter
        pipeline_def = [
            {'action': 'load_from_service', 'params': {'name': 'source1', 'output_name': 'df_initial'}},
            {'action': 'filter', 'params': {'name': 'df_initial', 'conditions': {'a': {'greater_than': 1}}, 'output_name': 'df_filtered'}}
        ]

        # Mock the load_from_service step to return initial_data
        self.mock_meta_data_service.get_data_source.return_value = {
            'meta': {},
            'db': Mock(query=Mock(return_value=initial_data))
        }
        self.mock_processor.load_from_data.return_value = initial_data

        # Execute
        result = self.executor.run(pipeline_def)

        # Assert
        self.mock_processor.filter.assert_called_once_with(initial_data, {'a': {'greater_than': 1}})
        self.assertIn('df_filtered', result)
        pd.testing.assert_frame_equal(result['df_filtered'], filtered_data)

  
    def test_join(self):
        # Setup
        df1 = pd.DataFrame({'key': [1, 2], 'value1': [10, 20]})
        df2 = pd.DataFrame({'key': [1, 2], 'value2': [30, 40]})
        joined_data = pd.merge(df1, df2, on='key')
        self.mock_processor.join.return_value = joined_data

        # Mock the MetaDataService to return a suitable dictionary
        self.mock_meta_data_service.get_data_source.return_value = {
            'meta': {},  # Mock metadata
            'db': Mock(query=Mock(return_value=df1))  # Mock database query
        }
        self.mock_processor.load_from_data.side_effect = [df1, df2]

        # Define a pipeline with mock load actions followed by join action
        pipeline_def = [
            {'action': 'load_from_service', 'params': {'name': 'source1', 'output_name': 'df1'}},
            {'action': 'load_from_service', 'params': {'name': 'source2', 'output_name': 'df2'}},
            {'action': 'join', 'params': {'name': 'df1', 'other_name': 'df2', 'on': 'key', 'output_name': 'df_joined'}}
        ]

        # Execute
        result = self.executor.run(pipeline_def)

        # Assert
        self.mock_processor.join.assert_called_once_with(df1, df2, 'key', 'inner')
        self.assertIn('df_joined', result)
        pd.testing.assert_frame_equal(result['df_joined'], joined_data)

    def test_select_columns(self):
        # Setup
        df = pd.DataFrame({'a': [1, 2], 'b': [3, 4], 'c': [5, 6]})
        selected_columns_df = df[['a', 'c']]
        self.mock_processor.select_columns.return_value = selected_columns_df
        self.mock_processor.load_from_data.return_value = df

        # Mock the MetaDataService to return a suitable dictionary
        self.mock_meta_data_service.get_data_source.return_value = {
            'meta': {},  # Mock metadata
            'db': Mock(query=Mock(return_value=df))  # Mock database query
        }

        # Define a pipeline with mock load actions followed by select_columns action
        pipeline_def = [
            {'action': 'load_from_service', 'params': {'name': 'source1', 'output_name': 'df'}},
            {'action': 'select_columns', 'params': {'name': 'df', 'columns': ['a', 'c'], 'output_name': 'df_selected'}}
        ]

        # Execute
        result = self.executor.run(pipeline_def)

        # Assert
        self.mock_processor.select_columns.assert_called_once_with(df, ['a', 'c'])
        self.assertIn('df_selected', result)
        pd.testing.assert_frame_equal(result['df_selected'], selected_columns_df)

    def test_rename_columns(self):
        # Setup
        df = pd.DataFrame({'old_name1': [1, 2], 'old_name2': [3, 4]})
        renamed_df = df.rename(columns={'old_name1': 'new_name1', 'old_name2': 'new_name2'})
        self.mock_processor.rename_columns.return_value = renamed_df
        self.mock_processor.load_from_data.return_value = df

        # Mock the MetaDataService to return a suitable dictionary
        self.mock_meta_data_service.get_data_source.return_value = {
            'meta': {},  # Mock metadata
            'db': Mock(query=Mock(return_value=df))  # Mock database query
        }

        # Define a pipeline with mock load actions followed by rename_columns action
        pipeline_def = [
            {'action': 'load_from_service', 'params': {'name': 'source1', 'output_name': 'df'}},
            {'action': 'rename_columns', 'params': {'name': 'df', 'rename_map': {'old_name1': 'new_name1', 'old_name2': 'new_name2'}, 'output_name': 'df_renamed'}}
        ]

        # Execute
        result = self.executor.run(pipeline_def)

        # Assert
        self.mock_processor.rename_columns.assert_called_once_with(df, {'old_name1': 'new_name1', 'old_name2': 'new_name2'})
        self.assertIn('df_renamed', result)
        pd.testing.assert_frame_equal(result['df_renamed'], renamed_df)

    def test_sort_data(self):
        # Setup
        df = pd.DataFrame({'a': [3, 1, 2]})
        sorted_df = df.sort_values(by='a')
        self.mock_processor.sort_data.return_value = sorted_df
        self.mock_processor.load_from_data.return_value = df

        # Mock the MetaDataService to return a suitable dictionary
        self.mock_meta_data_service.get_data_source.return_value = {
            'meta': {},  # Mock metadata
            'db': Mock(query=Mock(return_value=df))  # Mock database query
        }

        # Define a pipeline with mock load actions followed by sort_data action
        pipeline_def = [
            {'action': 'load_from_service', 'params': {'name': 'source1', 'output_name': 'df'}},
            {'action': 'sort_data', 'params': {'name': 'df', 'by': 'a', 'ascending': True, 'output_name': 'df_sorted'}}
        ]

        # Execute
        result = self.executor.run(pipeline_def)

        # Assert
        self.mock_processor.sort_data.assert_called_once_with(df, 'a', True)
        self.assertIn('df_sorted', result)
        pd.testing.assert_frame_equal(result['df_sorted'], sorted_df)

    def test_aggregate(self):
        # Setup
        df = pd.DataFrame({
            'group': ['A', 'A', 'B'],
            'value': [10, 20, 30]
        })
        aggregated_df = df.groupby('group').agg({'value': 'sum'}).reset_index()
        self.mock_processor.aggregate.return_value = aggregated_df
        self.mock_processor.load_from_data.return_value = df

        # Mock the MetaDataService to return a suitable dictionary
        self.mock_meta_data_service.get_data_source.return_value = {
            'meta': {},  # Mock metadata
            'db': Mock(query=Mock(return_value=df))  # Mock database query
        }

        # Define a pipeline with mock load actions followed by aggregate action
        pipeline_def = [
            {'action': 'load_from_service', 'params': {'name': 'source1', 'output_name': 'df'}},
            {'action': 'aggregate', 'params': {
                'name': 'df', 
                'group_by': ['group'], 
                'aggregations': {'value': 'sum'}, 
                'output_name': 'df_aggregated'
            }}
        ]

        # Execute
        result = self.executor.run(pipeline_def)

        # Assert
        self.mock_processor.aggregate.assert_called_once_with(df, ['group'], {'value': 'sum'})
        self.assertIn('df_aggregated', result)
        pd.testing.assert_frame_equal(result['df_aggregated'], aggregated_df)


    def test_add_columns(self):
        # Setup
        df = pd.DataFrame({'a': [1, 2]})
        new_columns_df = df.copy()
        new_columns_df['b'] = 3  # Using constant value instead of lambda
        new_columns_df['c'] = 4  # Another constant value
        self.mock_processor.add_columns.return_value = new_columns_df
        self.mock_processor.load_from_data.return_value = df

        # Mock the MetaDataService to return a suitable dictionary
        self.mock_meta_data_service.get_data_source.return_value = {
            'meta': {},  # Mock metadata
            'db': Mock(query=Mock(return_value=df))  # Mock database query
        }

        # Define a pipeline with mock load actions followed by add_columns action
        pipeline_def = [
            {'action': 'load_from_service', 'params': {'name': 'source1', 'output_name': 'df'}},
            {'action': 'add_columns', 'params': {
                'name': 'df', 
                'new_columns': {'b': 3, 'c': 4},  # Using constant values
                'output_name': 'df_with_new_columns'
            }}
        ]

        # Execute
        result = self.executor.run(pipeline_def)

        # Assert
        self.mock_processor.add_columns.assert_called_once_with(df, {'b': 3, 'c': 4})
        self.assertIn('df_with_new_columns', result)
        pd.testing.assert_frame_equal(result['df_with_new_columns'], new_columns_df)


    def test_apply_conditional_logic(self):
        # Setup
        df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        updated_df = df.copy()
        updated_df.loc[df['a'] > 1, 'b'] = 5
        self.mock_processor.apply_conditional_logic.return_value = updated_df
        self.mock_processor.load_from_data.return_value = df

        # Mock the MetaDataService to return a suitable dictionary
        self.mock_meta_data_service.get_data_source.return_value = {
            'meta': {},  # Mock metadata
            'db': Mock(query=Mock(return_value=df))  # Mock database query
        }

        # Define a pipeline with mock load actions followed by apply_conditional_logic action
        pipeline_def = [
            {'action': 'load_from_service', 'params': {'name': 'source1', 'output_name': 'df'}},
            {'action': 'apply_conditional_logic', 'params': {
                'name': 'df', 
                'condition_str': 'a > 1', 
                'update_values': {'b': 5}, 
                'output_name': 'df_updated'
            }}
        ]

        # Execute
        result = self.executor.run(pipeline_def)

        # Assert
        self.mock_processor.apply_conditional_logic.assert_called_once_with(df, 'a > 1', {'b': 5})
        self.assertIn('df_updated', result)
        pd.testing.assert_frame_equal(result['df_updated'], updated_df)

    def test_persist(self):
        # Setup
        df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        self.mock_processor.load_from_data.return_value = df

        # Mock the MetaDataService to return a suitable dictionary
        self.mock_meta_data_service.get_data_source.return_value = {
            'meta': {},  # Mock metadata
            'db': Mock(query=Mock(return_value=df))  # Mock database query
        }

        # Define a pipeline with mock load actions followed by persist action
        pipeline_def = [
            {'action': 'load_from_service', 'params': {'name': 'source1', 'output_name': 'df'}},
            {'action': 'persist', 'params': {
                'name': 'df', 
                'description': 'test description', 
                'category': 'test category'
            }}
        ]

        # Execute
        result = self.executor.run(pipeline_def)

        # Assert
        self.mock_meta_data_service.persist_data_source.assert_called_once_with('df', df, 'test description', 'test category')


    def test_complex_pipeline_1(self):
        # Setup initial data frames
        initial_df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]})
        filtered_df = initial_df[initial_df['a'] > 1]
        selected_df = filtered_df[['a', 'c']]
        renamed_df = selected_df.rename(columns={'a': 'alpha', 'c': 'gamma'})

        # Set return values for each processor method
        self.mock_processor.load_from_data.return_value = initial_df
        self.mock_processor.filter.return_value = filtered_df
        self.mock_processor.select_columns.return_value = selected_df
        self.mock_processor.rename_columns.return_value = renamed_df

        # Mock the MetaDataService
        self.mock_meta_data_service.get_data_source.return_value = {
            'meta': {}, 'db': Mock(query=Mock(return_value=initial_df))
        }

        # Define a complex pipeline
        pipeline_def = [
            {'action': 'load_from_service', 'params': {'name': 'source1', 'output_name': 'initial_df'}},
            {'action': 'filter', 'params': {'name': 'initial_df', 'conditions': {'a': {'greater_than': 1}}, 'output_name': 'filtered_df'}},
            {'action': 'select_columns', 'params': {'name': 'filtered_df', 'columns': ['a', 'c'], 'output_name': 'selected_df'}},
            {'action': 'rename_columns', 'params': {'name': 'selected_df', 'rename_map': {'a': 'alpha', 'c': 'gamma'}, 'output_name': 'final_df'}}
        ]

        # Execute
        result = self.executor.run(pipeline_def)

        # Assert
        self.mock_processor.load_from_data.assert_called_once()
        self.mock_processor.filter.assert_called_once_with(initial_df, {'a': {'greater_than': 1}})
        self.mock_processor.select_columns.assert_called_once_with(filtered_df, ['a', 'c'])
        self.mock_processor.rename_columns.assert_called_once_with(selected_df, {'a': 'alpha', 'c': 'gamma'})
        self.assertIn('final_df', result)
        pd.testing.assert_frame_equal(result['final_df'], renamed_df)

    def test_complex_pipeline_2(self):
        # Setup initial data frames
        initial_df = pd.DataFrame({'group': ['A', 'A', 'B'], 'value': [10, 20, 30], 'flag': [1, 1, 0]})
        aggregated_df = initial_df.groupby('group').agg({'value': 'sum'}).reset_index()
        added_columns_df = aggregated_df.copy()
        added_columns_df['new_column'] = 100
        conditional_logic_df = added_columns_df.copy()
        conditional_logic_df.loc[added_columns_df['group'] == 'A', 'new_column'] = 200

        # Set return values for each processor method
        self.mock_processor.load_from_data.return_value = initial_df
        self.mock_processor.aggregate.return_value = aggregated_df
        self.mock_processor.add_columns.return_value = added_columns_df
        self.mock_processor.apply_conditional_logic.return_value = conditional_logic_df

        # Mock the MetaDataService
        self.mock_meta_data_service.get_data_source.return_value = {
            'meta': {}, 'db': Mock(query=Mock(return_value=initial_df))
        }

        # Define another complex pipeline
        pipeline_def = [
            {'action': 'load_from_service', 'params': {'name': 'source2', 'output_name': 'initial_df'}},
            {'action': 'aggregate', 'params': {'name': 'initial_df', 'group_by': ['group'], 'aggregations': {'value': 'sum'}, 'output_name': 'aggregated_df'}},
            {'action': 'add_columns', 'params': {'name': 'aggregated_df', 'new_columns': {'new_column': 100}, 'output_name': 'added_columns_df'}},
            {'action': 'apply_conditional_logic', 'params': {'name': 'added_columns_df', 'condition_str': 'group == "A"', 'update_values': {'new_column': 200}, 'output_name': 'final_df'}}
        ]

         # Execute
        result = self.executor.run(pipeline_def)

        # Assert
        self.mock_processor.load_from_data.assert_called_once()
        self.mock_processor.aggregate.assert_called_once_with(initial_df, ['group'], {'value': 'sum'})
        self.mock_processor.add_columns.assert_called_once_with(aggregated_df, {'new_column': 100})
        self.mock_processor.apply_conditional_logic.assert_called_once_with(added_columns_df, 'group == "A"', {'new_column': 200})
        self.assertIn('final_df', result)
        pd.testing.assert_frame_equal(result['final_df'], conditional_logic_df)

 



    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
