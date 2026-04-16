from psycopg2 import connect
from config import host, database, user, password

def get_connection():
    try:
        conn = connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        return conn
    except Exception as error:
        print(f"Error connecting to database: {error}")
        return None