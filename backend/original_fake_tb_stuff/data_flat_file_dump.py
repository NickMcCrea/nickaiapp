import csv
import sqlite3
import sys

def dump_table_to_csv(connection, table_name, csv_file_path):
    # Query the database for the table and write its contents to a CSV file
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(columns)  # write headers
        csv_writer.writerows(rows)
    print(f"Data from {table_name} dumped to {csv_file_path}")
    cursor.close()

def main(db_path):
    # Connect to the SQLite database
    connection = sqlite3.connect(db_path)
    
    # Dump each table to a CSV file
    dump_table_to_csv(connection, 'counterparties', 'counterparties.csv')
    dump_table_to_csv(connection, 'nicktrialbalance', 'nicktrialbalance.csv')
    dump_table_to_csv(connection, 'products', 'products.csv')
    
    # Close the database connection
    connection.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python data_flat_file_dump.py <db_path>")
        sys.exit(1)
    
    db_path_arg = sys.argv[1]
    
    main(db_path_arg)
