import pandas as pd
import json

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
            'FLOAT': 'float64'
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


processor = DataProcessor()
trial_balance_df = processor.load('backend/datasources/nicktrialbalance.csv', 'backend/datasources/nicktrialbalance.json')
trial_balance_df = processor.filter(trial_balance_df, {'company_code': {'equals': '0302'}})
counterparties_df = processor.load('backend/datasources/counterparties.csv', 'backend/datasources/counterparties.json')
trial_balance_df = processor.join(trial_balance_df, counterparties_df, on='counterparty_id')

#just select the columns we need
trial_balance_df = processor.select_columns(trial_balance_df, ['company_code', 'counterparty_name', 'balance'])

# Now you can print or use the processed data as needed
print(trial_balance_df)

