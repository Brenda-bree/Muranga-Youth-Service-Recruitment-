import sqlite3
from config import DATABASE_PATH
from faker import Faker

fake = Faker()

def seed_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM recruitees")
    
    # Generate 10 people per cohort for cohorts 1-8
    records = []
    for cohort in range(1, 9):
        for _ in range(10):
            records.append((
                fake.unique.random_number(digits=9),  # id_number (9-digit numeric)
                fake.name(),                          # name
                fake.random_element(['M', 'F']),      # gender
                fake.random_element(['S', 'M', 'L', 'XL']),  # size
                fake.phone_number(),                  # phone_number
                cohort                                # cohort_number
            ))
    
    cursor.executemany('''
        INSERT INTO recruitees 
        (id_number, name, gender, size, phone_number, cohort_number)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', records)
    
    conn.commit()
    print(f"Inserted {len(records)} dummy records (10 per cohort, cohorts 1-8)")
    print("ID numbers are 9-digit numeric values (e.g., 425406665)")
    conn.close()

if __name__ == "__main__":
    seed_database()