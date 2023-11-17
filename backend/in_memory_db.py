import sqlite3
import pandas as pd
from typing import List, Dict, Any

class InMemoryDB:
    def __init__(self):
        """Initialize an in-memory SQLite database."""
        self.conn = sqlite3.connect(':memory:', check_same_thread=False)

    def load_csv_to_db(self, csv_path, meta_data):
        """
        Load CSV data into an in-memory database table, using metadata for type specification.
        
        :param csv_path: Path to the CSV file.
        :param meta_data: Metadata information including table name and field types.
        """

        ds_name = meta_data['name']
        field_types = {field['fieldName']: field['fieldType'] for field in meta_data['fields']}

        # Define pandas dtype mapping based on the field types
        pandas_dtypes = {
            'STRING': 'str',
            'INTEGER': 'Int64',  # Using Pandas nullable integer type
            'FLOAT': 'float',
            'DATE': 'str',  # Reading dates as strings initially to preserve formatting
            'BOOLEAN': 'boolean'
        }

        dtype_mapping = {column: pandas_dtypes[field_type] for column, field_type in field_types.items()}

        # Read the CSV data using pandas with specified dtypes
        df = pd.read_csv(csv_path, dtype=dtype_mapping)

        # Convert DATE fields to datetime after loading
        for column, field_type in field_types.items():
            if field_type == "DATE":
                df[column] = pd.to_datetime(df[column], errors='coerce')

        # Write the data into SQLite
        df.to_sql(ds_name, self.conn, if_exists='replace', index=False)

    def query(self, sql_query: str) -> List[Dict[str, Any]]:
        """
        Execute a SQL query on the in-memory database.

        :param sql_query: A SQL query string to execute.
        :return: The result of the query.
        """
        cur = self.conn.cursor()
        cur.execute(sql_query)

        columns = [column[0] for column in cur.description]
        results = [dict(zip(columns, row)) for row in cur.fetchall()]
        return results

    def close(self):
        """Close the connection to the in-memory database."""
        self.conn.close()

# Usage example:
# db = InMemoryDB()
# db.load_csv_to_db('path_to_your_csv.csv', 'spotify_data')
# results = db.query('SELECT * FROM spotify_data')
# for row in results:
#     print(row)
# db.close()
