from data_processor import DataProcessor


class DataPipelineExecutor:
    def __init__(self, processor : DataProcessor, pipeline_def):
        """
        Initialize the executor with a data processor and a pipeline definition.
        :param processor: An instance of DataProcessor or similar class with static methods for data operations.
        :param pipeline_def: A JSON-like dictionary defining the data processing pipeline.
        """
        self.processor = processor
        self.pipeline_def = pipeline_def

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
    

pipeline_definition = [
    {'action': 'load', 'params': {'name': 'trial_balance', 'filepath': 'backend/datasources/nicktrialbalance.csv', 'spec_path': 'backend/datasources/nicktrialbalance.json'}},
    {'action': 'filter', 'params': {'name': 'trial_balance', 'conditions': {'company_code': {'equals': '0302'}}}},
    {'action': 'load', 'params': {'name': 'counterparties', 'filepath': 'backend/datasources/counterparties.csv', 'spec_path': 'backend/datasources/counterparties.json'}},
    {'action': 'join', 'params': {'name': 'trial_balance', 'other_name': 'counterparties', 'on': 'counterparty_id'}},
    {'action': 'select_columns', 'params': {'name': 'trial_balance', 'columns': ['company_code', 'counterparty_name', 'balance']}}
   
]

executor = DataPipelineExecutor(DataProcessor, pipeline_definition)
result_data_frames = executor.run()

# Now you can print or use the processed data as needed
print(result_data_frames['trial_balance'])
