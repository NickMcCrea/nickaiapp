import os
from data_processor import DataProcessor
from meta_data_service import MetaDataService


class DataPipelineExecutor:
    def __init__(self, processor : DataProcessor, meta_data_service : MetaDataService):
        """
        Initialize the executor with a data processor and a pipeline definition.
        :param processor: An instance of DataProcessor or similar class with static methods for data operations.
        :param pipeline_def: A JSON-like dictionary defining the data processing pipeline.
        """
        self.processor = processor
        
        self.meta_data_service = meta_data_service

    def run(self, pipeline_def):
        """
        Execute the pipeline operations on the data as per the pipeline definition.
        """
        data_frames = {}

        for step in pipeline_def:
            action = step['action']
            params = step['params']

            if action == 'load_from_service':
                # Fetch data and metadata from the service
                data_source_name = params['data_source_name']
                data_source = self.meta_data_service.get_data_source(data_source_name)
                meta_data = data_source['meta']
                data = data_source['db'].query(f"SELECT * FROM {data_source_name}")
                data_frames[data_source_name] = self.processor.load_from_data(meta_data, data)
            
            
            elif action == 'filter':
                df_name = params['name']
                data_frames[df_name] = self.processor.filter(data_frames[df_name], params['conditions'])

            elif action == 'join':
                base_df_name = params['name']
                other_df_name = params['other_name']
                on = params['on']
                how = params.get('how', 'inner')
                data_frames[base_df_name] = self.processor.join(data_frames[base_df_name], data_frames[other_df_name], on, how)

            elif action == 'select_columns':
                df_name = params['name']
                columns = params['columns']
                data_frames[df_name] = self.processor.select_columns(data_frames[df_name], columns)

            elif action == 'rename_columns':
                df_name = params['name']
                rename_map = params['rename_map']
                data_frames[df_name] = self.processor.rename_columns(data_frames[df_name], rename_map)

            elif action == 'sort_data':
                df_name = params['name']
                by = params['by']
                ascending = params.get('ascending', True)
                data_frames[df_name] = self.processor.sort_data(data_frames[df_name], by, ascending)

            elif action == 'aggregate':
                df_name = params['name']
                group_by = params['group_by']
                aggregations = params['aggregations']
                data_frames[df_name] = self.processor.aggregate(data_frames[df_name], group_by, aggregations)

            elif action == 'persist':
                df_name = params['name']
                description = params.get('description', '')
                category = params.get('category', 'Your Data')
                self.meta_data_service.persist_data_source(df_name, data_frames[df_name], description, category)

            elif action == 'add_columns':
                df_name = params['name']
                new_columns = params['new_columns']
                data_frames[df_name] = self.processor.add_columns(data_frames[df_name], new_columns)

            elif action == 'apply_conditional_logic':
                df_name = params['name']
                condition_str = params['condition_str']
                update_values = params['update_values']
                data_frames[df_name] = self.processor.apply_conditional_logic(data_frames[df_name], condition_str, update_values)
            # Add more operations as needed

        return data_frames
    

    example_data_pipeline =  [
        {'action': 'load_from_service', 'params': {'data_source_name': 'source1'}},
        {'action': 'filter', 'params': {'name': 'source1', 'conditions': ['condition1', 'condition2']}},
        {'action': 'join', 'params': {'name': 'source1', 'other_name': 'source2', 'on': 'common_column', 'how': 'inner'}},
        {'action': 'select_columns', 'params': {'name': 'source1', 'columns': ['column1', 'column2']}},
        {'action': 'rename_columns', 'params': {'name': 'source1', 'rename_map': {'old_name1': 'new_name1', 'old_name2': 'new_name2'}}},
        {'action': 'sort_data', 'params': {'name': 'source1', 'by': 'sort_column', 'ascending': True}},
        {'action': 'aggregate', 'params': {'name': 'source1', 'group_by': ['group_column'], 'aggregations': {'column1': 'sum', 'column2': 'mean'}}},
        {'action': 'add_columns', 'params': {'name': 'source1', 'new_columns': {'new_column1': 'default_value1', 'new_column2': 'default_value2'}}},
        {'action': 'apply_conditional_logic', 'params': {'name': 'source1', 'condition_str': 'condition_expression', 'update_values': {'column1': 'new_value1', 'column2': 'new_value2'}}}
    ]








