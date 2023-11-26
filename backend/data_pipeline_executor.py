import os
from data_processor import DataProcessor
from meta_data_service import MetaDataService


class DataPipelineExecutor:
    def __init__(self, processor: DataProcessor, meta_data_service: MetaDataService):
        """
        Initialize the executor with a data processor and a meta data service.
        :param processor: An instance of DataProcessor or similar class with methods for data operations.
        :param meta_data_service: An instance of MetaDataService for handling meta data.
        """
        self.processor = processor
        self.meta_data_service = meta_data_service

    def run(self, pipeline_def):
        """
        Execute the pipeline operations on the data as per the pipeline definition.
        :param pipeline_def: A list of dictionaries defining the data processing pipeline.
        :return: A dictionary of data frames produced by the pipeline.
        """
        data_frames = {}

        for index, step in enumerate(pipeline_def):
            try:
                action = step['action']
                params = step['params']
                output_name = params.get('output_name', params['name'])

                if action == 'load_from_service':
                    data_source_name = params['name']
                    data_source = self.meta_data_service.get_data_source(data_source_name)
                    meta_data = data_source['meta']
                    data = data_source['db'].query(f"SELECT * FROM {data_source_name}")
                    data_frames[output_name] = self.processor.load_from_data(meta_data, data)

                elif action == 'filter':
                    input_name = params['name']
                    data_frames[output_name] = self.processor.filter(data_frames[input_name], params['conditions'])

                elif action == 'join':
                    base_df_name = params['name']
                    other_df_name = params['other_name']
                    on = params['on']
                    how = params.get('how', 'inner')
                    data_frames[output_name] = self.processor.join(data_frames[base_df_name], data_frames[other_df_name], on, how)

                elif action == 'select_columns':
                    input_name = params['name']
                    columns = params['columns']
                    data_frames[output_name] = self.processor.select_columns(data_frames[input_name], columns)

                elif action == 'rename_columns':
                    input_name = params['name']
                    rename_map = params['rename_map']
                    data_frames[output_name] = self.processor.rename_columns(data_frames[input_name], rename_map)

                elif action == 'sort_data':
                    input_name = params['name']
                    by = params['by']
                    ascending = params.get('ascending', True)
                    data_frames[output_name] = self.processor.sort_data(data_frames[input_name], by, ascending)

                elif action == 'aggregate':
                    input_name = params['name']
                    group_by = params['group_by']
                    aggregations = params['aggregations']
                    data_frames[output_name] = self.processor.aggregate(data_frames[input_name], group_by, aggregations)

                elif action == 'persist':
                    input_name = params['name']
                    description = params.get('description', '')
                    category = params.get('category', 'Your Data')
                    self.meta_data_service.persist_data_source(input_name, data_frames[input_name], description, category)

                elif action == 'add_columns':
                    input_name = params['name']
                    new_columns = params['new_columns']
                    data_frames[output_name] = self.processor.add_columns(data_frames[input_name], new_columns)

                elif action == 'apply_conditional_logic':
                    input_name = params['name']
                    condition_str = params['condition_str']
                    update_values = params['update_values']
                    data_frames[output_name] = self.processor.apply_conditional_logic(data_frames[input_name], condition_str, update_values)

            except Exception as e:
                raise RuntimeError(f"Error in pipeline at step {index + 1} ({action}): {e}") from e

            

        return data_frames

    

    example_data_pipeline = [
        {'action': 'load_from_service', 'params': {'name': 'source1', 'output_name': 'df_initial'}},
        {'action': 'filter', 'params': {'name': 'df_initial', 'conditions': {'column_name': {'in': ['value1', 'value2']}}, 'output_name': 'df_filtered'}},
        {'action': 'join', 'params': {'name': 'df_filtered', 'other_name': 'source2', 'on': 'common_column', 'how': 'inner', 'output_name': 'df_joined'}},
        {'action': 'select_columns', 'params': {'name': 'df_joined', 'columns': ['column1', 'column2'], 'output_name': 'df_selected_columns'}},
        {'action': 'rename_columns', 'params': {'name': 'df_selected_columns', 'rename_map': {'old_name1': 'new_name1', 'old_name2': 'new_name2'}, 'output_name': 'df_renamed'}},
        {'action': 'sort_data', 'params': {'name': 'df_renamed', 'by': 'sort_column', 'ascending': True, 'output_name': 'df_sorted'}},
        {'action': 'aggregate', 'params': {'name': 'df_sorted', 'group_by': ['group_column'], 'aggregations': [{'column': 'column1', 'aggregation': 'sum'}, {'column': 'column2', 'aggregation': 'mean'}], 'output_name': 'df_aggregated'}},
        {'action': 'add_columns', 'params': {'name': 'df_aggregated', 'new_columns': {'new_column1': 'default_value1', 'new_column2': 'default_value2'}, 'output_name': 'df_with_new_columns'}},
        {'action': 'apply_conditional_logic', 'params': {'name': 'df_with_new_columns', 'condition_str': 'condition_expression', 'update_values': {'column1': 'new_value1', 'column2': 'new_value2'}, 'output_name': 'df_final'}}
    ]









