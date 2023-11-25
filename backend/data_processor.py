import pandas as pd
import json
from meta_data_service import MetaDataService
import os

class DataProcessor:
    def __init__(self):
        self.data = {}


    

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
            df[date_column] = pd.to_datetime(df[date_column], errors='coerce')


        return df



    @staticmethod
    def filter(df, conditions):

          # Check if conditions is a dictionary
        if not isinstance(conditions, dict):
            raise TypeError("Conditions must be a dictionary.")
        
        """Apply various filter conditions to the data."""
        for column, condition in conditions.items():
            if not isinstance(condition, dict):
                raise ValueError("Each condition must be a dictionary.")

            if column not in df.columns:
                raise KeyError(f"Column '{column}' not found in DataFrame.")

            valid_keys = {'equals', 'greater_than', 'less_than', 'in', 'not_in', 'between', 'not_equals'}
            if not any(key in condition for key in valid_keys):
                raise ValueError("Condition does not contain a valid key.")

            try:
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
            except Exception as e:
                raise ValueError(f"Error processing condition for column '{column}': {str(e)}")

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
    
    @staticmethod
    def add_columns(df, new_columns):
        """Add new columns to the DataFrame.
        
        Args:
            df (pd.DataFrame): The original DataFrame.
            new_columns (dict): A dictionary where keys are new column names 
                                and values are either constants or functions 
                                that take the DataFrame as input and return a Series.
        
        Returns:
            pd.DataFrame: The DataFrame with new columns added.
        """
        for column_name, value in new_columns.items():
            if callable(value):
                df[column_name] = value(df)
            else:
                df[column_name] = value
        return df
    
    @staticmethod
    def apply_conditional_logic(df, condition_str, update_values):
        """Apply conditional logic to set values in columns based on a string condition.
        
        Args:
            df (pd.DataFrame): The original DataFrame.
            condition_str (str): A string representing the condition to be evaluated.
            update_values (dict): A dictionary where keys are column names and values are the values to set.
        
        Returns:
            pd.DataFrame: The DataFrame after applying conditional logic.
        """
        mask = df.query(condition_str).index
        for column, value in update_values.items():
            df.loc[mask, column] = value
        return df



    


# desired_cwd = os.path.abspath(os.path.join(os.path.dirname(__file__)))
# os.chdir(desired_cwd)

#meta_data_service = MetaDataService()
#meta_data_service.add_data_source('backend/datasources/counterparties.json', 'backend/datasources/counterparties.csv')
# tb_data_source_name = 'trial_balance_data'
# tb_data_source = meta_data_service.get_data_source(tb_data_source_name)
# tb_meta_data = tb_data_source['meta']
# tb_data = tb_data_source['db'].query(f"SELECT * FROM {tb_data_source_name}")  

# #filter tb on company code 0302
# tb_data = DataProcessor.load_from_data(tb_meta_data, tb_data)
# tb_data = DataProcessor.filter(tb_data, {'company_code': {'equals': '0302'}})

#let's load counterparty data now
# cp_data_source_name = 'counterparty_data'

# cp_data_source = meta_data_service.get_data_source(cp_data_source_name)
# cp_meta_data = cp_data_source['meta']
# cp_data = cp_data_source['db'].query(f"SELECT * FROM {cp_data_source_name}")
# cp_data = DataProcessor.load_from_data(cp_meta_data, cp_data)
# cp_data = DataProcessor.execute_sql(cp_data, "counterparty_data", "UPDATE counterparty_data SET counterparty_name = 'Yolo'")
# print(cp_data)
# #let's join the two data sources
# joined_data = DataProcessor.join(tb_data, cp_data, on='counterparty_id', how='left')

# #let's select the columns we want
# joined_data = DataProcessor.select_columns(joined_data, ['company_code',  'counterparty_name',  'balance', 'pnl_date'])
# print(joined_data)


