import sqlalchemy as db
from faker import Faker
import sys
from datetime import datetime
import json
import os
from gics import GICSGen
from products import ProductGenerator
import random


# Initialise Faker
fake = Faker()
gics_gen = GICSGen()

# Map from SQL types to Faker methods
FAKER_METHODS = {
    "VARCHAR(255)": lambda: fake.word(),
    "INTEGER": lambda: fake.random_int(min=1, max=100),
    "COMPANY_NAME": lambda: fake.company(), 
    "COUNTRY_CODE": lambda: fake.country_code(),
    "REAL": lambda: round(fake.random_number(digits=5) / 100.0, 2),
    "DATE": lambda: datetime.strptime(fake.date(), "%Y-%m-%d").date()
}



# Parse command line arguments - 1st is the path, second is the number of rows to generate
if len(sys.argv) != 3:
    print("Usage: python data_generator.py <path> <num_rows>")
    sys.exit(1)

path = sys.argv[1]
num_rows = int(sys.argv[2])

# Define the number of unique ids you want to generate
num_unique_ids = (int)(num_rows / 10)  # Adjust to your needs

# Generate unique ids for counterparty_id, product_id, and account
counterparty_ids = [str(fake.unique.random_number(digits=9, fix_len=True)) for _ in range(num_unique_ids)]
product_ids = [str(fake.unique.random_number(digits=9, fix_len=True)) for _ in range(num_unique_ids)]
accounts = [str(fake.unique.random_number(digits=9, fix_len=True)) for _ in range(num_unique_ids)]

fake.unique.clear()  # Clear Faker's uniqueness tracking

# Check if the database file exists
if os.path.exists('database.db'):
    # If it does, remove it
    os.remove('database.db')

# Connect to the database
engine = db.create_engine('sqlite:///database.db')
connection = engine.connect()
metadata = db.MetaData()

acceptable_values_dict = {}

# Iterate over files in path
for filename in os.listdir(path):
    if filename.endswith(".ddl"):
        print(f"Processing {filename}")
        ddl_file = os.path.join(path, filename)
        accept_values_file = os.path.join(path, filename.replace(".ddl", ".json"))

        # Read the DDL file
        with open(ddl_file, "r") as f:
            ddl = f.read()

        # Read acceptable values if the file exists
        if os.path.isfile(accept_values_file):
            with open(accept_values_file, 'r') as f:
                acceptable_values_dict[filename.replace(".ddl", "")] = json.load(f)
                print(f"Loaded acceptable values: {acceptable_values_dict}")

        # Execute the DDL, and print out any errors
        try:
            connection.execute(db.text(ddl))
            metadata.reflect(bind=engine)
        except Exception as e:
            print(e)
            continue  # Move to next file if there was an error

def generate_row(table_name, columns, id_value=None):
    """Generates a row of data for a table."""
    row_data = {}
    acceptable_values = acceptable_values_dict.get(table_name, {})

    gics_levels = gics_gen.get_random_gics()

    random_prod = ProductGenerator().get_random_product()

    for col in columns:
        col_type = str(col.type)
        if col.name in acceptable_values:
            row_data[col.name] = fake.random_element(acceptable_values[col.name])
            if col.name == "pnl_date":
                row_data[col.name] = datetime.strptime(row_data[col.name], "%Y-%m-%d").date()
        elif col.name == "product_id":
            if id_value:
                row_data[col.name] = id_value
            else:
                # Choose a random product_id from the pre-generated list
                row_data[col.name] = random.choice(product_ids)
        elif col.name == "counterparty_id":
            if id_value:
                row_data[col.name] = id_value
            else:
                # Choose a random counterparty_id from the pre-generated list
                row_data[col.name] = random.choice(counterparty_ids)
        elif col.name == "account":
            if id_value:
                row_data[col.name] = id_value
            else:
                # Choose a random account from the pre-generated list
                row_data[col.name] = random.choice(accounts)
        elif col.name == "counterparty_name":
            row_data[col.name] = FAKER_METHODS["COMPANY_NAME"]()
        elif col.name == "country_of_organisation" or col.name == "country_of_jurisdiction" or col.name == "country_of_residence":
            row_data[col.name] = FAKER_METHODS["COUNTRY_CODE"]()

        elif col.name == "gics_level_1":
            row_data[col.name] = gics_levels[0]
        elif col.name == "gics_level_2":
            row_data[col.name] = gics_levels[1]
        elif col.name == "gics_level_3":
            row_data[col.name] = gics_levels[2]
        elif col.name == "gics_level_4":
            row_data[col.name] = gics_levels[3]

        elif col.name == "product_type":
            row_data[col.name] = random_prod[0]
        elif col.name == "instrument_type":
            row_data[col.name] = random_prod[1]
        elif col.name == "market_type":
            row_data[col.name] = random_prod[2]
        elif col.name == "contract_type":
            row_data[col.name] = random_prod[3]
        elif col.name == "risk_type":
            row_data[col.name] = random_prod[4]

        elif col_type in FAKER_METHODS:
            row_data[col.name] = FAKER_METHODS[col_type]()
        else:
            print(f"Warning: No Faker method found for column type '{col_type}'. Using None.")
            row_data[col.name] = None
    return row_data

# Define table objects
Counterparties = metadata.tables['counterparties']
Products = metadata.tables['products']
NickTrialBalance = metadata.tables['nicktrialbalance']

# Generate data for each table
for _ in range(num_rows):
    # Generate a row for NickTrialBalance
    row_data = generate_row('nicktrialbalance', NickTrialBalance.columns)
    connection.execute(NickTrialBalance.insert(), row_data)
   

    product_id = row_data.get("product_id")
    counterparty_id = row_data.get("counterparty_id")

    product_exists = connection.execute(db.select(Products).where(Products.c.product_id == product_id)).fetchone()
    counterparty_exists = connection.execute(db.select(Counterparties).where(Counterparties.c.counterparty_id == counterparty_id)).fetchone()

    # If not, generate a new row for them
    if not product_exists:
        product_data = generate_row('products', Products.columns, product_id)
        connection.execute(Products.insert(), product_data)

    if not counterparty_exists:
        counterparty_data = generate_row('counterparties', Counterparties.columns, counterparty_id)
        connection.execute(Counterparties.insert(), counterparty_data)

# Build a select statement that joins the three tables on their common fields
stmt = db.select('*').select_from(
    NickTrialBalance
    .join(Counterparties, NickTrialBalance.c.counterparty_id == Counterparties.c.counterparty_id)
    .join(Products, NickTrialBalance.c.product_id == Products.c.product_id)
).limit(5)

# Execute the statement and fetch all results
results = connection.execute(stmt).fetchall()

# Print out the results
print("Join query: \n")
for row in results:
    print(row)

connection.commit()

# Close the connection
connection.close()
