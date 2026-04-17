import sqlite3
from config import DATABASE_PATH

def get_db_connection():
    """Creates and returns a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Create the recruitees and users tables if they don't exist"""
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
    
    # Users table for authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('staff', 'admin')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database tables 'recruitees' and 'users' ready.")

def get_user_by_username(username):
    """Fetch a user by username"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


#to help the admin get logged in staff
def get_all_users():
    """Fetch all users (excluding passwords)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role, created_at FROM users ORDER BY created_at DESC")
    users = cursor.fetchall()
    conn.close()
    return users

def create_user(username, hashed_password, role):
    """Create a new user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, hashed_password, role) VALUES (?, ?, ?)",
            (username, hashed_password, role)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def delete_user_by_id(user_id):
    """Delete a user by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0


def get_all_recruitees(limit=100):
    """Fetch all recruitees (for admin listing)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_number, name, gender, size, phone_number, cohort_number FROM recruitees ORDER BY cohort_number, name LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_recruitee_by_id(id_number):
    """Fetch a single recruitee by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recruitees WHERE id_number = ?", (id_number,))
    row = cursor.fetchone()
    conn.close()
    return row

def add_recruitee(id_number, name, gender, size, phone_number, cohort_number):
    """Add a new recruitee"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO recruitees (id_number, name, gender, size, phone_number, cohort_number) VALUES (?, ?, ?, ?, ?, ?)",
            (id_number, name, gender, size, phone_number, cohort_number)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def update_recruitee(id_number, name, gender, size, phone_number, cohort_number):
    """Update an existing recruitee"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE recruitees SET name = ?, gender = ?, size = ?, phone_number = ?, cohort_number = ? WHERE id_number = ?",
        (name, gender, size, phone_number, cohort_number, id_number)
    )
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def delete_recruitee(id_number):
    """Delete a recruitee by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recruitees WHERE id_number = ?", (id_number,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def update_user_password(user_id, hashed_password):
    """Update a user's password"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET hashed_password = ? WHERE id = ?", (hashed_password, user_id))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0


def get_user_by_username(username):
    """Fetch a user by username"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    """Fetch a user by ID (excludes password)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role, created_at FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_all_users():
    """Fetch all users (excluding passwords)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role, created_at FROM users ORDER BY created_at DESC")
    users = cursor.fetchall()
    conn.close()
    return users

def create_user(username, hashed_password, role):
    """Create a new user"""
    import sqlite3
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, hashed_password, role) VALUES (?, ?, ?)",
            (username, hashed_password, role)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def delete_user_by_id(user_id):
    """Delete a user by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def update_user_password(user_id, hashed_password):
    """Update a user's password"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET hashed_password = ? WHERE id = ?", (hashed_password, user_id))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0