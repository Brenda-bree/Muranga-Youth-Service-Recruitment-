import sqlite3
from config import DATABASE_PATH

def get_db_connection():
    """Creates and returns a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Create the recruitees table if it doesn't exist"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recruitees (
            id_number TEXT PRIMARY KEY,
            name TEXT,
            gender TEXT,
            size TEXT,
            phone_number TEXT,
            cohort_number INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database table 'recruitees' ready.")