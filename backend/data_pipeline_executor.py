import os
from data_processor import DataProcessor
from meta_data_service import MetaDataService


class DataPipelineExecutor:
    def __init__(self, processor : DataProcessor, pipeline_def, meta_data_service : MetaDataService):
        """
        Initialize the executor with a data processor and a pipeline definition.
        :param processor: An instance of DataProcessor or similar class with static methods for data operations.
        :param pipeline_def: A JSON-like dictionary defining the data processing pipeline.
        """
        self.processor = processor
        self.pipeline_def = pipeline_def
        self.meta_data_service = meta_data_service

    def run(self):
        """
        Execute the pipeline operations on the data as per the pipeline definition.
        """
        data_frames = {}

        for step in self.pipeline_def:
            action = step['action']
            params = step['params']

            if action == 'load':
                data_frames[params['name']] = self.processor.load(params['filepath'], params['spec_path'])

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

            # Add more operations as needed

        return data_frames


desired_cwd = os.path.abspath(os.path.join(os.path.dirname(__file__)))
os.chdir(desired_cwd)   

pipeline_definition = [
    {'action': 'load_from_service', 'params': {'data_source_name': 'trial_balance_data'}},
    {'action': 'filter', 'params': {'name': 'trial_balance_data', 'conditions': {'company_code': {'equals': '0302'}}}},
    {'action': 'load_from_service', 'params': {'data_source_name': 'counterparty_data'}},
    {'action': 'join', 'params': {'name': 'trial_balance_data', 'other_name': 'counterparty_data', 'on': 'counterparty_id'}},
    {'action': 'select_columns', 'params': {'name': 'trial_balance_data', 'columns': ['company_code', 'counterparty_name', 'balance']}}
]

meta_data_service = MetaDataService()  # Instantiate the MetaDataService
executor = DataPipelineExecutor(DataProcessor, pipeline_definition, meta_data_service)
result_data_frames = executor.run()

print(result_data_frames['trial_balance_data'])
