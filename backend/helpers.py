# helpers.py
import json
from sqlalchemy import text
from termcolor import colored

def get_table_names(db_session):
    """Return a list of table names."""
    table_names = []
    tables = db_session.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
    for table in tables.fetchall():
        table_names.append(table[0])
    return table_names

def get_column_names(db_session, table_name):
    """Return a list of column names."""
    column_names = []
    columns = db_session.execute(text(f"PRAGMA table_info('{table_name}');")).fetchall()
    for col in columns:
        column_names.append(col[1])
    return column_names

def get_database_info(db_session):
    """Return a list of dicts containing the table name and columns for each table in the database."""
    table_dicts = []
    for table_name in get_table_names(db_session):
        columns_names = get_column_names(db_session, table_name)
        table_dicts.append({"table_name": table_name, "column_names": columns_names})
    return table_dicts

def execute_query(db_session, query):
    """Function to query SQLite database with a provided SQL query."""
    try:
        resultproxy = db_session.execute(text(query))
        # get the column names
        keys = resultproxy.keys()
        # get the row data
        resultset = resultproxy.fetchall()
        # create a list of dictionaries
        results = [dict(zip(keys, row)) for row in resultset]
    except Exception as e:
        results = f"query failed with error: {e}"
    return results


def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }
    
    for message in messages:
        if message["role"] == "system":
            print(colored(f"system: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "user":
            print(colored(f"user: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and message.get("function_call"):
            print(colored(f"assistant: {message['function_call']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and not message.get("function_call"):
            print(colored(f"assistant: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "function":
            print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))

def extract_info_from_messages(messages):
    input_query = None
    sql_query = None
    result_set = None

    #get the last message in the array
    message = messages[-1]

    if message["role"] == "user":
        input_query = message["content"]
    elif message["role"] == "assistant" and message.get("function_call"):
        sql_query = json.loads(message["function_call"]["arguments"])["query"]
    elif message["role"] == "function":
        result_set = message["content"]
    
    return input_query, sql_query, result_set
