import pandas as pd
import json
from meta_data_service import MetaDataService

class DataProcessor:
    def __init__(self):
        self.data = {}

        

    @staticmethod
    def load(filepath, spec_path):
        """Load a CSV file with specified data types based on a JSON spec."""
        with open(spec_path, 'r') as spec_file:
            spec = json.load(spec_file)
            dtype_mapping, parse_dates = DataProcessor._parse_dtype_spec(spec['fields'])

        return pd.read_csv(filepath, dtype=dtype_mapping, parse_dates=parse_dates)
    

    @staticmethod
    def load_from_data(meta_data, data):
        """Load data from metadata and data source result."""
        dtype_mapping, parse_dates = DataProcessor._parse_dtype_spec(meta_data['fields'])

        # Create the DataFrame without enforcing dtypes
        df = pd.DataFrame(data)

        # Apply dtypes for non-date columns
        for column, dtype in dtype_mapping.items():
            if column not in parse_dates:  # Exclude date columns from astype
                df[column] = df[column].astype(dtype, errors='ignore')

        # Parse dates explicitly for date columns
        for date_column in parse_dates:
            df[date_column] = pd.to_datetime(df[date_column], errors='coerce', format='%Y-%m-%d')

        return df



    @staticmethod
    def filter(df, conditions):
        """Apply various filter conditions to the data."""
       
        for column, condition in conditions.items():
            if 'equals' in condition:
                df = df[df[column] == condition['equals']]
            elif 'greater_than' in condition:
                df = df[df[column] > condition['greater_than']]
            elif 'less_than' in condition:
                df = df[df[column] < condition['less_than']]
            elif 'in' in condition:
                df = df[df[column].isin(condition['in'])]
            elif 'not_in' in condition:
                df = df[~df[column].isin(condition['not_in'])]
            elif 'between' in condition:
                lower, upper = condition['between']
                df = df[df[column].between(lower, upper)]
            elif 'not_equals' in condition:
                df = df[df[column] != condition['not_equals']]
            # Add more condition types as needed
        return df

    @staticmethod
    def _parse_dtype_spec(fields):
        """Parse field specifications to create a dtype mapping and parse_dates list for Pandas."""
        dtype_map = {
            'STRING': 'object',
            'INTEGER': 'Int64',  # Allows for missing values
            'FLOAT': 'float64',
        }
        dtype_mapping = {}
        parse_dates = []
        for field in fields:
            if field['fieldType'] == 'DATE':
                parse_dates.append(field['fieldName'])
            else:
                dtype_mapping[field['fieldName']] = dtype_map.get(field['fieldType'], 'object')
        return dtype_mapping, parse_dates



    @staticmethod
    def join(df1, df2, on, how='inner'):
        """Join two datasets."""
        return pd.merge(df1, df2, on=on, how=how)

    @staticmethod
    def aggregate(df, group_by, aggregations):
        """Aggregate data."""
        aggregation_dict = {item['column']: item['aggregation'] for item in aggregations}
        return df.groupby(group_by).agg(aggregation_dict).reset_index()

    @staticmethod
    def select_columns(df, columns):
        """Select specific columns from the data."""
        return df[columns]

    @staticmethod
    def rename_columns(df, rename_map):
        """Rename columns in the data."""
        return df.rename(columns=rename_map)

    @staticmethod
    def sort_data(df, by, ascending=True):
        """Sort data based on given columns."""
        return df.sort_values(by=by, ascending=ascending)



meta_data_service = MetaDataService()
tb_data_source_name = 'trial_balance_data'
tb_data_source = meta_data_service.get_data_source(tb_data_source_name)
tb_meta_data = tb_data_source['meta']
tb_data = tb_data_source['db'].query(f"SELECT * FROM {tb_data_source_name}")  
#print(tb_data)




# Load data into DataFrame
trial_balance_df = DataProcessor.load_from_data(tb_meta_data, tb_data)
print(trial_balance_df)

trial_balance_from_csv = DataProcessor.load('backend/datasources/nicktrialbalance.csv', 'backend/datasources/nicktrialbalance.json')
print(trial_balance_from_csv)



