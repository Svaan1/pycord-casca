from sqlalchemy import create_engine
from default import Config

config = Config().database

class Database():
    def __init__(self, table_name):
        self.database_engine = create_engine(f"{config['dialect']}://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['dbname']}")
        self.table_name = table_name
        self.create_tables()

    def create_tables(self):
        self.database_engine.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER NOT NULL,
            money INTEGER,
            PRIMARY KEY (id)
)''')