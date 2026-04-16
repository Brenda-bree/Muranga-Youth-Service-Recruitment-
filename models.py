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
    
    # Insert a record into the database
    cursor.execute('''
        INSERT OR IGNORE INTO recruitees 
        (id_number, name, gender, size, phone_number, cohort_number)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('placeholder', 'placeholder', 'placeholder', 'placeholder', 'placeholder', 0))

        # Count how many records are in the database
    cursor.execute('SELECT COUNT(*) as count FROM recruitees')
    result = cursor.fetchone()
    print(f"Total records in database: {result['count']}")
    
    conn.commit()
    conn.close()
    print("Load cohort data function ready.")