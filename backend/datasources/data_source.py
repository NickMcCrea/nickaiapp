import json

class DataSource:
    def __init__(self, name, description, type, connectionInfo, tables):
        self.name = name
        self.description = description
        self.type = type
        self.connectionInfo = connectionInfo
        self.tables = tables

    def __str__(self):
        return json.dumps({
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'connectionInfo': self.connectionInfo,
            'tables': self.tables
        }, indent=4)
