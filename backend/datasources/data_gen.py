import json
import csv
import random
from datetime import datetime, timedelta

# Function to generate a random date
def random_date():
    start_date = datetime(2000, 1, 1)
    end_date = datetime.today()
    time_between_dates = end_date - start_date
    random_number_of_days = random.randrange(time_between_dates.days)
    return start_date + timedelta(days=random_number_of_days)

# Load JSON data from a file
def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to generate data for a field
def generate_data(field_type, field_name, custom_values):
    if field_type == "INTEGER":
        return random.randint(1, 1000)
    elif field_type == "FLOAT":
        return round(random.uniform(1.0, 1000.0), 2)
    elif field_type == "STRING":
        if field_name in custom_values and custom_values[field_name]:
            return random.choice(custom_values[field_name])
        else:
            return f"Random_{field_name}_{random.randint(1, 1000)}"
    elif field_type == "DATE":
        if field_name in custom_values and custom_values[field_name]:
            # Assuming custom date values are in 'YYYY-MM-DD' format
            date_str = random.choice(custom_values[field_name])
            # Convert string to date and back to string to ensure correct formatting
            return datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
        else:
            return random_date().strftime('%Y-%m-%d')
    else:
        return "Unknown"

# Function to generate data rows
def generate_data_rows(json_spec, custom_values, num_rows):
    data = []
    for _ in range(num_rows):
        row = {}
        for field in json_spec["fields"]:
            field_name = field["fieldName"]
            field_type = field["fieldType"]
            row[field_name] = generate_data(field_type, field_name, custom_values)
        data.append(row)
    return data

# File paths for JSON specifications
json_spec_file_path = 'backend\datasources\glbal.json'  # Replace with your JSON spec file path
custom_values_file_path = 'backend\datasources\glbal_values.json'  # Replace with your custom values file path

# Load JSON data from files
json_spec = load_json_data(json_spec_file_path)
custom_values = load_json_data(custom_values_file_path)  # This will be an empty dict if the file is not found

# Generate data rows
num_rows = 1000  # specify the number of rows you want to generate
generated_data = generate_data_rows(json_spec, custom_values, num_rows)

# Write data to a CSV file
csv_file_name = 'backend/datasources/glbal.csv'
with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=[field["fieldName"] for field in json_spec["fields"]])
    writer.writeheader()
    writer.writerows(generated_data)

print(f"Data written to {csv_file_name}")
