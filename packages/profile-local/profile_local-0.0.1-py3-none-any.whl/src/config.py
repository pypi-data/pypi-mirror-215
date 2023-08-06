from dotenv import load_dotenv
load_dotenv()
from circles_local_database_python.database import database 

def db_connection(schema):
        # Connect to the MySQL database
        database_conn = database()
        db = database_conn.connect_to_database()
        db.database = schema
        return db

