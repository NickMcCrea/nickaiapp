from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import backend.helpers as helpers

class DBWrapper:
    def __init__(self, db_path):
        # create a pool of connections
        self.engine = create_engine(db_path, connect_args={'check_same_thread': False}, pool_pre_ping=True)
        self.db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))
        
        # Get the database schema
        self.database_schema_dict = helpers.get_database_info(self.db_session)
        self.database_schema_string = self._get_database_schema_string()

    def _get_database_schema_string(self):
        return "\n".join(
            [
                f"Table: {table['table_name']}\nColumns: {', '.join(table['column_names'])}"
                for table in self.database_schema_dict
            ]
        )
