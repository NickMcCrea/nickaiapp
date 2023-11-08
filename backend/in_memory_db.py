import sqlite3
import pandas as pd
from typing import List, Dict, Any

class InMemoryDB:
    def __init__(self):
        """Initialize an in-memory SQLite database."""
        self.conn = sqlite3.connect(':memory:', check_same_thread=False)

    def load_csv_to_db(self, csv_path, table_name):
        """
        Load CSV data into an in-memory database table.
        
        :param csv_path: Path to the CSV file.
        :param table_name: Name of the table to create in the database.
        """
        # Read the CSV data using pandas
        df = pd.read_csv(csv_path)
        # Write the data into SQLite
        df.to_sql(table_name, self.conn, if_exists='replace', index=False)

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
