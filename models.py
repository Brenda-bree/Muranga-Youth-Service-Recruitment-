import sqlite3
from config import DATABASE_PATH

def get_db_connection():
    """
    Creates and returns a connection to the SQLite database.
    This function is called whenever we need to talk to the database.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  
    return conn

def init_database():
    """
    create tables
    """
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
    
    print("Database table 'recruitees' created with fields: name, id_number, gender, size, phone_number, cohort_number")

def load_cohort_data():
    """
    Loads all 8 cohorts of existing recruitees into the database.
    YOU ONLY RUN THIS ONCE when setting up the system.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Data loading to go her
    
    conn.commit()
    conn.close()
    print("Load cohort data function ready.")