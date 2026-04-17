import bcrypt  
from models import get_db_connection  
  
def create_admin():  
    username = input("Enter admin username: ").strip()  
    password = input("Enter admin password: ").strip()  
  
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  
  
    conn = get_db_connection()  
    cursor = conn.cursor()  
    try:  
        cursor.execute(  
            "INSERT INTO users (username, hashed_password, role) VALUES (?, ?, ?)",  
            (username, hashed.decode('utf-8'), 'admin')  
        )  
        conn.commit()  
        print(f"Admin user '{username}' created successfully.")  
    except Exception as e:  
        print(f"Error: {e}")  
    finally:  
        conn.close()  
  
if __name__ == "__main__":  
    create_admin() 
